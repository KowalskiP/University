/*
  refrlejs.js - Javascript implementation of RLE encode/decode algorithm
  Copyright (C) 2009 Mark Lomas

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

// RLE decompression reference implementation
function rleDecode(data)
{
	var result = new Array;
	if(data.length == 0)
		return result;

	if((data.length % 2) != 0)
	{
		alert("Invalid RLE data");
		return;
	}

	for(var i = 0; i < data.length; i+=2)
	{
		var val = data[i];
		var count = data[i+1];
		for(var c = 0; c < count; c++)
			result[result.length] = val;
	}
	return result;
}

// RLE compression reference implementation
function rleEncode(data)
{
	var result = new Array;
	if(data.length == 0)
		return result;

	var count = 1;
	var r = 0;
	for(var i = 0; i < (data.length - 1); i++)
	{
		if(data[i] != data[i+1])
		{
			result[r] = data[i];
			result[r+1] = count;
			count = 0;
			r +=2;
		}
		count++;
	}
	result[r] = data[i];
	result[r+1] = count;

	return result;
}

var test = [0,0,0,1,1,1,2,2,2,1,3,3,3,3,0];
WScript.StdOut.WriteLine("Original");
for(var i = 0; i < test.length; i++)
    WScript.StdOut.Write(test[i] + ",");

var result = rleEncode(test);

WScript.StdOut.WriteLine("\nEncoded");
for(var i = 0; i < result.length; i++)
    WScript.StdOut.Write(result[i] + ",");

WScript.StdOut.WriteLine("\nDecoded");
var decoded = rleDecode(result);
for(var i = 0; i < decoded.length; i++)
    WScript.StdOut.Write(decoded[i] + ",");
