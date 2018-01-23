/**
 * Created by Антон on 21.04.2015.
 */
import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.Map;


public class Server {
    static final int PORT = 31337;
    static final String ROOT = "FTP";
    public static final Object SYN = new Object();
    static String ROOT_PATH;

    public static void main(String[] args) throws IOException{
        File dir = new File(ROOT);
        dir.mkdirs();
        ROOT_PATH = dir.getAbsolutePath();
        System.out.println(ROOT_PATH);
        ServerSocket s = new ServerSocket(PORT);
        System.out.println("FTP Server started");
        try{
            while (true){
                Socket socket = s.accept();
                try {
                    new ServeClient(socket);
                }catch (IOException e){
                    e.printStackTrace();
                    socket.close();
                }
            }
        }
        finally {
            s.close();
        }
    }

}

class ServeClient extends Thread{
    private Socket socket;
    private DataInputStream  dis;
    private  DataOutputStream dos;
    private int buffSize = 64*1024;
    private byte [] buffer = new byte[buffSize];
    private String PATH;

    public ServeClient(Socket s)throws IOException{
        socket = s;
        dis = new DataInputStream(socket.getInputStream());
        dos = new DataOutputStream(socket.getOutputStream());
//        System.setProperty("user.dir", System.getProperty("user.dir") +'\\'+ Server.ROOT);
        PATH = Server.ROOT_PATH;
        start();
    }

    public void run(){
        try{
            String s = "";
//            dos.writeUTF("HELLO");
//            dos.flush();
            while (!s.equalsIgnoreCase("quit")){
                s = dis.readUTF();
//                System.out.println(s);
                proc(s);
            }
            System.out.println("Closed " + socket);
        }catch (IOException e){
            e.printStackTrace();
            System.err.println("IO Exception");
        }finally {
            try{
                socket.close();
            }catch (IOException e){
                e.printStackTrace();
                System.err.println("Socket not closed");
            }
        }
    }

    private void pwd() throws IOException{
//        String s = System.getProperty("user.dir");
        dos.writeUTF(PATH);
        dos.flush();
    }
    private void ls() throws IOException{
        File folder = new File(PATH);
        File [] files = folder.listFiles();
        if (files != null) {
            dos.writeInt(files.length);
            for (File file : files) {
                if (file.isFile()){
                    dos.writeUTF("FILE: " +file.getName());
                } else {
                    dos.writeUTF("DIR: " +file.getName());
                }
            }
        }
        else {
            dos.writeInt(0);
        }
        dos.flush();
    }
    private void cd(String c) throws IOException{
//        String cd = System.getProperty("user.dir");
//        System.out.println(cd);
        if (c.equals(".") || c.equals(PATH)){
            dos.writeUTF("Completed");
        } else if(c.equals("..")){
            int p = PATH.lastIndexOf('\\');
            String nd = PATH.substring(0,p);
            System.out.println(PATH);
            System.out.println(nd.contains(Server.ROOT_PATH));
            System.out.println(Server.ROOT_PATH.contains(nd));
            if (nd.contains(Server.ROOT_PATH)) {
                System.out.println(nd);
                File f = new File(nd);
//                System.setProperty("user.dir", f.getAbsolutePath());
                PATH = f.getAbsolutePath();
                dos.writeUTF("Completed");
            }
            else {
                dos.writeUTF("Out of ROOT");
            }
        } else {
            File f = new File(PATH + '\\' + c);
            if (f.isDirectory()) {
//                System.setProperty("user.dir", f.getAbsolutePath());
                PATH = f.getAbsolutePath();
                dos.writeUTF("Completed");
            } else {
                dos.writeUTF("FILE is not a DIR");
            }
        }
        dos.flush();
    }
    private void put(String c) throws IOException{
        int count = 0,total = 0;
        Long size = dis.readLong();
        System.out.println("Received: " + c +" FROM: " + socket);
        File f = null;
        FileWriter outF = null;
        synchronized (Server.SYN){
            f = makefile(c);
            outF = new FileWriter(f);
        }
        String str = "";
        while ((count = dis.read(buffer)) != -1){
            total += count;
            str += new String(buffer, 0 , count);
            if (total == size)
                break;
        }
        outF.write(str);
        outF.flush();
        outF.close();
        System.out.println("Created: " + c + " FROM: " + f.getName());
        dos.writeUTF("Completed");
    }
    private void get(String c) throws IOException{
//        String cd = System.getProperty("user.dir");
        System.out.println(c);
        File f = new File(PATH + '\\' + c);
        dos.writeLong(f.length());
        BufferedInputStream bis = new BufferedInputStream(new FileInputStream(f));
        int count;
        while((count = bis.read(buffer))!=-1){
            System.out.println(1);
            dos.write(buffer, 0, count);
            System.out.println(2);
        }
        System.out.println(3);
//        dos.writeUTF("Completed");
        System.out.println(4);
        dos.flush();
        bis.close();
    }

    public void proc(String comand) throws IOException{
        Map<String, Integer> commands = new HashMap<String,Integer>();
        commands.put("pwd", 1);
        commands.put("ls", 3);
        commands.put("cd", 5);
        commands.put("lcd", 6);
        commands.put("put", 7);
        commands.put("get", 8);
        commands.put("quit", 9);
        System.out.println(comand);
        String [] temp = comand.split(" ");
//        System.out.println(temp[1]);

        switch (commands.get(temp[0])){
            case  1:
                pwd();
                break;
            case  3:
                ls();
                break;
            case  5:
                cd(temp[1]);
                break;

            case  7:
                put(temp[1]);
                break;
            case  8:
                get(temp[1]);
                break;
//            case  9:

        }
    }

    private File makefile(String filename){
        String n = filename;
//        String cd = System.getProperty("user.dir");
        File f = new File(PATH + '\\' + filename);
        System.out.println(f.getAbsolutePath());
        int count =0;
        while (f.exists()){
//            System.out.println(n);
            String [] temp = filename.split("\\.");
            count += 1;
            n = temp[0] + '(' + count + ")." + temp[1];
            System.out.println(n);
            f = new File(PATH + '\\' + n);
        }
        return f;
    }
}