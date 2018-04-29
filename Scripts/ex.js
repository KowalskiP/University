/*fso = new ActiveXObject("Scripting.FileSystemObject");
fh = fso.OpenTextFile("E:\\first.txt");
s = '';

while (!fh.AtEndOfStream){
	s += fh.ReadLine();
	s += '\n';
}
WSH.echo(s);
fh.Close();

fh = fso.OpenTextFile("E:\\first.txt", 2, true);
f.WriteLine("Test Line");
f.Close();

WSH.echo(WScript.Arguments.length)
WSH.echo(WScript.Arguments(1))
*/

s = WScript.StdIn.ReadLine();
WSH.echo(s);