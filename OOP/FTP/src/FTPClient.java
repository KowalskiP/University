/**
 * Created by Антон on 21.04.2015.
 */
import java.io.*;
import java.net.*;
import java.util.*;

public class FTPClient {
    private DataInputStream dis;
    public DataOutputStream dos;
    private int buffSize = 64*1024;
    private byte [] data = new byte[buffSize];
    private Scanner input = new Scanner(System.in);
    private final Object SYN = new Object();

    public FTPClient(String address) throws IOException{
        Socket s = new Socket(address, Server.PORT);
        dis = new DataInputStream(s.getInputStream());
        dos = new DataOutputStream(s.getOutputStream());
    }

    public void main()throws IOException{
//        String addr = "127.0.0.1";
//        String addr = address;
//        Socket s = new Socket(addr, Server.PORT);
//        dis = new DataInputStream(s.getInputStream());
//        dos = new DataOutputStream(s.getOutputStream());
//        System.out.println("socket = " + s);
        String str = "";
//        System.out.println(str);
        while (!str.equalsIgnoreCase("quit")){
            System.out.print(">> ");
            str = input.nextLine();
            proc(str);
        }
        System.out.println("Closed");
    }

    private void pwd(String c) throws IOException{
        dos.writeUTF(c);
        dos.flush();
        String s = dis.readUTF();
        System.out.println(s);
    }
    public String [] ls(String c) throws IOException{
        dos.writeUTF(c);
        dos.flush();
        int l = dis.readInt();
        String [] ss=new String[l];
        for (int i=0;i<l;i++){
            String str = dis.readUTF();
            ss[i]=str;
            System.out.println(str);
        }
        return ss;
    }
    private void lls() throws IOException{
        File folder = new File(System.getProperty("user.dir"));
        File [] files = folder.listFiles();
        if (files!=null){
            for (File file: files){
                if (file.isFile()){
                    System.out.println("FILE: " + file.getName());
                } else {
                    System.out.println("DIR:  "  + file.getName());
                }
            }
        }
    }
    public void cd(String c) throws IOException{
        dos.writeUTF(c);
        dos.flush();
        String str = dis.readUTF();
        System.out.println(str);
    }
    private void lcd(String c) throws IOException{
        String cd = System.getProperty("user.dir");
        System.out.println(cd);
        if (c.equals(".")){
            System.out.println("Completed");
        } else if(c.equals("..")){
            int p = cd.lastIndexOf('\\');
            String nd = cd.substring(0,p);
            System.out.println(nd);
            File f = new File(nd);
            System.setProperty("user.dir", f.getAbsolutePath());
            System.out.println("Completed");

        } else {
            File f = new File(cd + '\\' + c);
            if (f.isDirectory()) {
                System.setProperty("user.dir", f.getAbsolutePath());
                System.out.println("Completed");
            } else {
                System.out.println("FILE is not a DIR");
            }
        }
    }
    private void printHelp(){
        System.out.println("This is a FTP Server:");
        System.out.println("pwd  - print current work dir on server");
        System.out.println("lpwd - print current work dir on client");
        System.out.println("ls   - print list of files in current dir on server");
        System.out.println("lls  - print list of files in current dir on client");
        System.out.println("cd   - change current work dir on server");
        System.out.println("lcd  - change current work dir on client");
        System.out.println("put  - upload file to server");
        System.out.println("get  - download file from server");
        System.out.println("quit - disconnect from server");
        System.out.println("help - print this help");

    }
    public void put(String c) throws IOException{
        dos.writeUTF("put " + c);
        File f = new File(c);
        dos.writeLong(f.length());
        BufferedInputStream bis = new BufferedInputStream(new FileInputStream(f));
        int count;
        while((count = bis.read(data))!=-1){
            dos.write(data, 0, count);
        }
        dos.flush();
        bis.close();
        String ans = dis.readUTF();
        System.out.println(ans);
    }
    public void get(String c) throws IOException{
        int count = 0,total = 0;
        dos.writeUTF("get " + c);
        dos.flush();
        Long size = dis.readLong();
        System.out.println(size);
        File f = null;
        FileWriter outF = null;
        synchronized (SYN){
            f = makefile(c);
            outF = new FileWriter(f);
        }
        System.out.println(3);
        String str = "";
        while ((count = dis.read(data)) != -1){
            System.out.println(4);
            System.out.println(data.toString());
            System.out.println(count);
            total += count;
            str += new String(data, 0 , count);
            System.out.println(total);
            System.out.println(size);
            if (total == size)
                System.out.println(5);
                break;
        }
        System.out.println(4);
        outF.write(str);
        outF.flush();
        outF.close();
        System.out.println("5");
//        String ans = dis.readUTF();
//        System.out.println(ans);
    }

    public void proc(String comand) throws IOException{
        Map<String, Integer> commands = new HashMap<String,Integer>();
        commands.put("pwd",  1);
        commands.put("lpwd", 2);
        commands.put("ls", 3);
        commands.put("lls", 4);
        commands.put("cd", 5);
        commands.put("lcd", 6);
        commands.put("put", 7);
        commands.put("get", 8);
        commands.put("quit", 9);
        commands.put("help", 10);
        String [] temp = comand.split(" ");
        if (!commands.containsKey(temp[0])){
            System.out.println("This command not available: " + comand);
            System.out.println("Please print 'help'");
            return;
        }
        switch (commands.get(temp[0])){
            case  1:
                pwd(temp[0]);
                break;
            case  2:
                System.out.println(System.getProperty("user.dir"));
                break;
            case  3:
                ls(temp[0]);
                break;
            case  4:
                lls();
                break;
            case  5:
                cd(comand);
                break;
            case  6:
                lcd(temp[1]);
                break;
            case  7:
                put(temp[1]);
                break;
            case  8:
                get(temp[1]);
                break;
            case  9:
                dos.writeUTF(temp[0]);
                dos.flush();
                break;
            case 10:
                printHelp();
                break;
        }
    }

    private File makefile(String filename){
        String n = filename;
        String cd = System.getProperty("user.dir");
        File f = new File(cd + '\\' + filename);
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
}
