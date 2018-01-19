import System.Environment
import System.IO
-- import System.Directory
-- import Control.Concurrent
-- import Control.Monad
import Network
import qualified Data.ByteString.Lazy as BSL

getResponse :: Handle -> IO()
getResponse handle = do
	resp <- hGetLine handle
	let [status, count] = words resp
	case status of
		"ERR" -> putStrLn "Error:"
		"OK" -> return ()
		_ -> error "Corrupted response"
	getLinesFromHandle handle (read count :: Int)

getLinesFromHandle :: (Num s, Eq s) => Handle -> s -> IO ()
getLinesFromHandle _ 0 = return ()
getLinesFromHandle handle n = do
	hGetLine handle >>= putStrLn
	getLinesFromHandle handle $ n - 1	 

parseGET :: Handle -> FilePath -> IO()
parseGET handle fileName = do
    file <- openFile fileName WriteMode
    hSetBinaryMode file True
    hPutStrLn handle $ "get " ++ fileName
    hFlush handle
    resp <- hGetLine handle
    case words resp of
        ["OK", size] -> do
            hSetBinaryMode handle True
            fileContent <- BSL.hGet handle  (read size :: Int)
            BSL.hPut file fileContent
            hFlush file
        ["ERR", liness] ->
            getLinesFromHandle handle (read liness :: Int)
    hClose file
    hSetBinaryMode handle False
 
parsePUT :: Handle -> FilePath -> IO()
parsePUT handle fileName = do
    file <- openFile fileName ReadMode
    hSetBinaryMode file True
    fileSize <- hFileSize file
    hPutStrLn handle $ "put " ++ fileName
    hFlush handle
    getResponse handle
    hPrint handle $ show fileSize
    hFlush handle
    hSetBinaryMode handle True
    fileContent <- BSL.hGetContents file
    BSL.hPut handle fileContent
    hClose file
    hSetBinaryMode handle False


client :: Handle -> IO()
client handle = do
    str <- getLine
    let cmd = head (words str)
    let args = unwords $ drop 1 $ words str
    case cmd of
        "get" -> do
            parseGET handle args
            client handle
        "put" -> do
            parsePUT handle args
            client handle
        "dir" -> do
			hPutStrLn handle str
			hFlush handle
			getResponse handle
			client handle
        "cd" -> do
            hPutStrLn handle str
            hFlush handle
            getResponse handle
            client handle
        "quit" -> do
            hPutStrLn handle str
            hFlush handle
            getResponse handle
            hClose handle
        _ -> do
            putStrLn $ "Unknown command or bad syntax: " ++ str
            client handle

main :: IO()
main = withSocketsDo $ do
    args <- getArgs
    case args of
        [host, port] -> do
			sock <- connectTo host $ PortNumber $ fromIntegral (read port :: Int)
			hSetBuffering sock $ BlockBuffering $ Just 4096
			putStrLn "Connection complete"
			client sock
        _ -> putStrLn "Usage\nFtpClient <host> <port>"
