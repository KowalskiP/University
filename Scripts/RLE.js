/***************************/
/**********RLE.js***********/
/**Кодирование длин серий***/
/***************************/

//считывание аргументов командной строки
var arg = WScript.Arguments;
 
 //открытие файла и считывание текста
fso = new ActiveXObject("Scripting.FileSystemObject");
fhi = fso.OpenTextFile(arg.item(0));
temp = fhi.ReadAll();
fhi.close();
//WSH.echo(temp+'\n');
//кодирование
	var str="";
	var i=0;
	l=temp.length;
	while (i<l){
		var j=i;
		while ((j<l) && (temp.charAt(i)==temp.charAt(j+1))) j++;
		if (temp.charAt(i)=="#"){
			str+="#"+String.fromCharCode(j-i+1)+temp.charAt(i);
			i+=j-i+1;
			//WSH.echo(i+' '+j+' '+'c1\n');
		}
		else{
			if (j-i+1<=3){
				str+=temp.charAt(i);
				i++;
				//WSH.echo(i+' '+j+' '+'c2\n');
			}
			else{
				k=j-i+1;
				//WSH.echo(k+'\n');
				if (k>259){
					while (k>259){
						str+="#"+String.fromCharCode(255)+temp.charAt(i);
						i+=259;
						//WSH.echo(i+' '+j+' '+'c3\n');
						k-=259;
					}
				}
				str+="#"+String.fromCharCode(j-i+1)+temp.charAt(i);
				i+=j-i+1;
				//WSH.echo(i+' '+j+' '+'c4\n');
			}
		}
	}
	
WSH.echo(str);
//декодирование
