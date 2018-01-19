import System.Environment
import System.IO
import System.Directory
import Control.Concurrent
import Control.Monad
import Control.Exception hiding (handle)
import Network
import qualified Data.ByteString.Lazy as BSL


parseDIR :: String -> Handle -> IO()
parseDIR root handle = do
    files <- getDirectoryContents root
    formatedFiles <- forM files formatFile
    hPutStrLn handle  $ "OK " ++ show (length formatedFiles)
    forM_ formatedFiles (hPutStrLn handle)
    hFlush handle
    where
    formatFile file = do
        canonicalName <- canonicalizePath $ root ++ "/" ++ file
        isDirectory <- doesDirectoryExist canonicalName 
        if isDirectory then
            return $ "<DIR>  " ++ show file ++ "  0"
        else do
            h <- openFile canonicalName ReadMode
            fileSize <- hFileSize h
            return $ "<FILE> " ++ show file ++ "  " ++ show fileSize


parseGET :: String -> String -> Handle -> IO()
parseGET root fileName handle = do
    canonicalName <- canonicalizePath $ root ++ "/" ++ fileName
    fileHandler <- openFile canonicalName ReadMode

    hSetBinaryMode fileHandler True
    fileSize <- hFileSize fileHandler
    fileContent <- BSL.hGetContents fileHandler
    hPutStrLn handle $ "OK " ++ show fileSize
    hFlush handle
    hSetBinaryMode handle True
    BSL.hPut handle fileContent
    hFlush handle

    hSetBinaryMode handle False
    hClose fileHandler


parsePUT :: String -> String -> Handle -> IO()
parsePUT root fileName handle = do
    fileHandler <- openFile (root ++ "/" ++ fileName) WriteMode

    hSetBinaryMode fileHandler True
    hPutStrLn handle "OK 0"
    hFlush handle
    fileSize <- fmap (read :: String -> Int) $ hGetLine handle
    hSetBinaryMode handle True
    fileContent <- BSL.hGet handle fileSize
    BSL.hPut fileHandler fileContent
    hSetBinaryMode handle False
    hFlush fileHandler

    hClose fileHandler


parseCD :: String -> String -> Handle -> IO FilePath
parseCD root args handle = do
    newDirectory <- canonicalizePath $ root ++ "/" ++ args
    exist <- doesDirectoryExist newDirectory
    if not exist then
        error "Directory not exits"
    else do
        hPutStrLn handle "OK 1"
        hPutStrLn handle newDirectory
        hFlush handle
        return newDirectory


handleException :: Handle -> SomeException -> IO ()
handleException handle e = do
    hPutStrLn handle $ "ERR 1\n" ++ show (e :: SomeException)
    hFlush handle


serveOneClient :: String -> Handle -> IO()
serveOneClient root handle = do
    str <- hGetLine handle
    let cmd = head (words str)
    let args = unwords $ drop 1 $ words str
    case cmd of
        "get" -> do
            parseGET root args handle `catch` handleException handle 
            serveOneClient root handle
        "put" -> do
            parsePUT root args handle `catch` handleException handle 
            serveOneClient root handle
        "dir" -> do
            parseDIR root handle `catch` handleException handle 
            serveOneClient root handle
        "cd" -> do
            newDirectory <- parseCD root args handle `catch` \e -> do
                hPutStrLn handle $ "ERR 1\n" ++ show (e :: SomeException)
                hFlush handle
                return root
            serveOneClient newDirectory handle 
        "quit" -> do
            hPutStrLn handle "OK 1"
            hPutStrLn handle "Bye!"
            hFlush handle
            hClose handle


main :: IO()
main = withSocketsDo $ do
    args <- getArgs
    case args of
        [root, port] -> do
            sock <- listenOn $ PortNumber $ fromIntegral (read port :: Int)
            forever $ do
                (handle, hostName, _) <- accept sock
                hSetBuffering handle $ BlockBuffering $ Just 4096
                putStrLn $ hostName ++ ":" ++ port ++ " connected..."
                canonicalName <- canonicalizePath root
                createDirectoryIfMissing True canonicalName
                forkIO $ serveOneClient canonicalName handle
        _ -> putStrLn "Usage\nFtpServer <root_directory> <port>"
