import java.io.IOException;

/**
 * Created by Антон on 22.04.2015.
 */
public class RunClient {
    public static void main(String[] args) throws IOException{
        FTPClient f = new FTPClient("127.0.0.1");
        f.main();
    }
}
