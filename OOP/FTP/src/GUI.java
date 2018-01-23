/**
 * Created by Антон on 23.04.2015.
 */
import java.io.*;
import com.trolltech.qt.gui.*;

public class GUI extends QWidget{

    private FTPClient ftp;
    private QFrame frameClient;
    private QFrame frameServer;
    private QLabel lblClient;
    private QLabel lblServer;
    private QTextEdit fieldClient;
    private QTextEdit fieldServer;
    private QListWidget listClient;
    private QListWidget listServer;
    private QPushButton btnClient;
    private QPushButton btnServer;
    private QPushButton btnCDsr;
    private QPushButton btnCDcl;

    public GUI(FTPClient ftpc){
        ftp = ftpc;
        setWindowTitle("FTP client");
        resize(640, 480);
        QHBoxLayout bs = new QHBoxLayout();
        setLayout(bs);

        QGridLayout cl = new QGridLayout();
        QGridLayout sr = new QGridLayout();

        frameClient = new QFrame(this);
        frameClient.setLayout(cl);

        frameServer = new QFrame(this);
        frameServer.setLayout(sr);

        lblClient = new QLabel("Client");
        fieldClient = new QTextEdit(System.getProperty("user.dir"));
        listClient = new QListWidget();
        btnClient = new QPushButton(">>");
        btnCDcl = new QPushButton("Set");
        fieldClient.setMaximumSize(300, 25);
        cl.addWidget(lblClient, 0, 0);
        cl.addWidget(fieldClient,1,0);
        cl.addWidget(btnCDcl, 1, 1);
        cl.addWidget(listClient,2,0,1,2);
        cl.addWidget(btnClient,3,0,1,2);

        lblServer = new QLabel("Server");
        fieldServer = new QTextEdit();
        listServer = new QListWidget();
        btnServer = new QPushButton("<<");
        btnCDsr = new QPushButton("Set");
        fieldServer.setMaximumSize(300,25);
        sr.addWidget(lblServer, 0, 0);
        sr.addWidget(fieldServer, 1, 0);
        sr.addWidget(btnCDsr,1,1);
        sr.addWidget(listServer,2,0,1,2);
        sr.addWidget(btnServer,3,0,1,2);

        bs.addWidget(frameClient);
        bs.addWidget(frameServer);


        listClient.itemDoubleClicked.connect(this, "printPath()");
        listServer.itemDoubleClicked.connect(this, "printPathS()");
        btnCDcl.clicked.connect(this, "CDCl()");
        btnCDsr.clicked.connect(this, "CDSr()");
        btnClient.clicked.connect(this, "putFile()");
        btnServer.clicked.connect(this, "getFile()");
        btnCDcl.click();
        btnCDsr.click();


    }

    @Override
    protected void closeEvent(QCloseEvent arg__1) {
        try {
            ftp.dos.writeUTF("quit");
        }
        catch (IOException e){
            e.printStackTrace();
        }
        super.closeEvent(arg__1);
    }
    public void printPathS(){
//        System.out.println(1);
        String [] dir = listServer.selectedItems().get(0).text().split(" ");
//        System.out.println(dir[0].equals("DIR:"));
        if (dir[0].equals("DIR:")){
//            System.out.println(dir[1]);
            fieldServer.setText(dir[1]);
        }
    }

    public void printPath(){
        String dir = listClient.selectedItems().get(0).text().split(" ")[1];
        File f = new File(System.getProperty("user.dir") + '\\' + dir);
        if (f.isDirectory()){
            if (dir.equals(".")){
                fieldClient.setText(System.getProperty("user.dir"));
            } else if (dir.equals("..")){
                String cd = System.getProperty("user.dir");
                int p = cd.lastIndexOf("\\");
                String nd = cd.substring(0, p);
                fieldClient.setText(nd);
            }else
                fieldClient.setText(f.getPath());
        }
    }

    public void putFile() throws IOException{
        String fileName = listClient.selectedItems().get(0).text().split(" ")[1];
        File f = new File(fileName);
        if (!f.isDirectory()) {
            System.out.println(fileName);
            ftp.put(fileName);
        }
        btnCDsr.click();
    }

    public void getFile() throws IOException{
        String fileName = listServer.selectedItems().get(0).text().split(" ")[1];
        File f = new File(fileName);
        if (!f.isDirectory()){
            ftp.get(fileName);
        }
        btnCDcl.click();
    }

    public void CDSr() throws IOException{
        listServer.clear();
        String dir = fieldServer.toPlainText();
        if (!dir.equals("")) {
            ftp.cd("cd " + dir);
        }
        String [] ss = ftp.ls("ls");
        for (String s: ss){
            listServer.addItem(s);
        }
        listServer.addItem("DIR: .");
        listServer.addItem("DIR: ..");
        listServer.sortItems();
    }

    public void CDCl(){
        listClient.clear();
        String dir = fieldClient.toPlainText();
        File d = new File(dir);
        if (d.exists()){
            System.out.println(d.getPath());
            System.setProperty("user.dir", d.getAbsolutePath());
            File [] files = d.listFiles();
            if (files != null)
            for (File file: files){
                if (file.isDirectory()){
                    listClient.addItem("DIR: " + file.getName());
                }
                else
                {
                    listClient.addItem("FILE: " + file.getName());
                }
            }
        }
        listClient.addItem("DIR: .");
        listClient.addItem("DIR: ..");
        listClient.sortItems();
    }

    public static void main(String[] args) throws IOException{
        QApplication.initialize(args);

        FTPClient ftp = new FTPClient("127.0.0.1");

        GUI gui = new GUI(ftp);
        gui.show();

        QApplication.execStatic();
    }

}
