import java.io.*;


public class Encoder {

	public static void main(String[] args) 
	{
	
		File 
			f1 = new File(args[0]),
			f2 = new File(args[2]),
			of = new File(args[4]);
		
		String 
			cp1 = args[1], 
			cp2 = args[3],
			ncp1 = args[5],
			ncp2 = args[6];

        System.out.println(args[0]);
        int counter = 0;
		String line = null;
		byte[] buff;
		
		try {
		
			BufferedReader br1 = new BufferedReader(
					new InputStreamReader(new FileInputStream(f1), cp1));
			BufferedReader br2 = new BufferedReader(
					new InputStreamReader(new FileInputStream(f2), cp2));
			FileOutputStream fout = new FileOutputStream(of);
			
			try {
				
				while (true) {
					if (counter % 2 == 0) {
						line = br1.readLine();
						if (line == null) 
							break;
						buff = line.getBytes(ncp1);
					} else {
						line = br2.readLine();
						if (line == null) 
							break;
						buff = line.getBytes(ncp2);
					}
					fout.write(buff);
					fout.write('\n');
					counter++;
				}
				
			} finally {
				fout.close();
				br1.close();
				br2.close();
			}
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
