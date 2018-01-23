import java.io.*;


public class Threads
{
    public static void main (String args[]) throws InterruptedException
    {
        String fn1;
        String fn2;
        try{
            fn1 = args[0];
            fn2 = args[1];
        }catch (IndexOutOfBoundsException e){
            System.out.println("java Threads input_file output_file");
            return;
        }

        Copier copier = new Copier (
                fn1,
                fn2,
                4096);
        System.out.println("Всего скопированно: " + copier.start().join().getTotalCounter());
    }
}

class Copier
{
    private int bufferCount;
    private long totalCounter;
    private final Thread readingThread;
    private final Thread writingThread;
    private byte[] buffer;

    public Copier (final String inputFile, final String outputFile, int bufferSize)
    {
        buffer = new byte[bufferSize];
        readingThread = new Thread(new Runnable() {
            @Override
            public void run ()
            {
                try {
                    FileInputStream fis = new FileInputStream(inputFile);
                    try {
                        for (;;) {
                            synchronized (Copier.this) {
                                if (bufferCount == 0) {
                                    bufferCount = fis.read(buffer);
                                }
                                if (bufferCount == -1) {
                                    break;
                                }
                            }
                        }
                    }
                    finally {
                        fis.close();
                    }
                }
                catch (IOException ex) {
                    bufferCount = -1;
                    ex.printStackTrace();
                }
            }
        });
        writingThread = new Thread(new Runnable() {
            @Override
            public void run ()
            {
                try {
                    FileOutputStream fos = new FileOutputStream(outputFile);
                    try {
                        for (;;) {
                            synchronized (Copier.this) {
                                if (bufferCount > 0) {
                                    fos.write(buffer, 0, bufferCount);
                                    totalCounter += bufferCount;
                                    bufferCount = 0;
                                }
                                if (bufferCount == -1) {
                                    break;
                                }
                            }
                        }
                    }
                    finally {
                        fos.close();
                    }
                }
                catch (IOException ex) {
                    bufferCount = -1;
                    ex.printStackTrace();
                }
            }
        });
    }

    public Copier start ()
    {
        readingThread.start();
        writingThread.start();
        return this;
    }

    public Copier join () throws InterruptedException
    {
        readingThread.join();
        writingThread.join();
        return this;
    }

    public long getTotalCounter ()
    {
        return totalCounter;
    }
}