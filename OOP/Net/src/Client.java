/**
 * Created by Антон on 13.04.2015.
 */
import java.net.*;

import java.io.*;

public class Client {
    public static void main(String[] args) throws IOException {
//        String inName;
//        String addr;
//        try {
//            addr = args[0];
//            inName = args[1];
//        }   catch(ArrayIndexOutOfBoundsException ex) {
//            System.out.println("java Client address fileName");
//            return;
//        }
//        File inputFile = new File(inName);
        File inputFile = new File("file.txt");
        String addr = "127.0.0.1";
        int fileLength = (int) inputFile.length();
        byte [] data = new byte [fileLength];

//        InetAddress addr = InetAddress.getByName(null);
        System.out.println("addr = " + addr);
        Socket socket = new Socket(addr, 31337);

        try {
            BufferedInputStream bis = new BufferedInputStream(new FileInputStream(inputFile));
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
            System.out.println("socket = " + socket);

            dos.writeLong(fileLength);
            dos.writeUTF(inputFile.getName());
            int count;
            while ((count = bis.read(data)) != -1){
                dos.write(data, 0, count);
            }
            dos.flush();
            bis.close();
            dos.close();
        }
        finally {
            System.out.println("closing...");

            socket.close();
        }
    }
}