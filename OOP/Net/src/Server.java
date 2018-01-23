/**
 * Created by Антон on 13.04.2015.
 */
import java.io.*;

import java.net.*;

class ServeOneJabber extends Thread {
    private Socket socket;
//    private BufferedReader in;
//    private PrintWriter out;
    private DataInputStream din;
    private int buffSize;

    public ServeOneJabber(Socket s) throws IOException {
        socket = s;
        din = new DataInputStream(socket.getInputStream());
        buffSize = socket.getReceiveBufferSize();
        // Включаем автоматическое выталкивание:
//        out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket
//                .getOutputStream())), true);
        // Если любой из вышеприведенных вызовов приведет к
        // возникновению исключения, то вызывающий отвечает за
        // закрытие сокета. В противном случае, нить
        // закроет его.
        start(); // вызываем run()
    }

    private File makefile(String filename){
        String n = filename;
        File f = new File(filename);
        int count =0;
        while (f.exists()){
//            System.out.println(n);
            String [] temp = filename.split("\\.");
            count += 1;
            n = temp[0] + '(' + count + ")." + temp[1];
            f = new File(n);
        }
        return f;
    }

    public void run() {
        try {
            byte [] data = new byte[buffSize];
            int count = 0,total = 0;
            while (true) {
                long size = din.readLong();
                String fileName = din.readUTF();
                System.out.println("Received " + fileName);
                String newName = fileName;
                File f = null;
                FileWriter outF = null;
                synchronized (Server.syn){

                    f = makefile(newName);
                    outF = new FileWriter(f);


                }
                String str = "";
                while ((count = din.read(data)) != -1){
                    total += count;
                    str += new String(data, 0 , count);
                    if (total == size)
                        break;
                }
                outF.write(str);
                outF.flush();
                outF.close();
//                File f = new File(newName);
//                while (f.exists()){
//                    String [] temp = fileName.split("\\.");
//                    count += 1;
//                    newName = temp[0] + '(' + count + ")." + temp[1];
//                    f = new File(newName);
//                }
                System.out.println("Created " + f.getName());
                break;

//                String str = in.readLine();
//                if (str.equals("END"))
//                    break;
//                System.out.println("Echoing: " + str);
//                out.println(str);
            }
            System.out.println("closing...");
        }
        catch (IOException e) {
            e.printStackTrace();
            System.err.println("IO Exception");
        }
        finally {
            try {
                socket.close();
            }
            catch (IOException e) {
                System.err.println("Socket not closed");
            }
        }
    }
}

public class Server {
    static final int PORT = 31337;
    static Object syn = new Object();

    public static void main(String[] args) throws IOException {
        ServerSocket s = new ServerSocket(PORT);
        System.out.println("Server Started");
        try {
            while (true) {
                // Блокируется до возникновения нового соединения:
                Socket socket = s.accept();
                try {
                    new ServeOneJabber(socket);
                }
                catch (IOException e) {
                    // Если завершится неудачей, закрывается сокет,
                    // в противном случае, нить закроет его:
                    socket.close();
                }
            }
        }
        finally {
            s.close();
        }
    }
}
