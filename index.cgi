#!/bin/bash

FILE=""

if ! [ -z "$DOCUMENT_URI" ];then
	if [[ $DOCUMENT_URI =~ ^(/[a-zA-Z0-9/]+)?/?$ ]];then
		[[ $DOCUMENT_URI =~ ^/?$ ]]&&DOCUMENT_URI="/index/"
		FILE=data${DOCUMENT_URI%%/}
		if [ -d "$FILE" ];then
			FILE=$FILE/index
		fi
		FILE=$FILE.md
		if ! [ -f "$FILE" ];then
			FILE=""
		fi
	fi
fi

if [ -z "$FILE" ];then
	cat << "END"
Content-Type: text/html
Server: 404.exe

<html>
<head><title>404 Not Found</title></head>
<body bgcolor="white">
<center><h1>404 Not Found</h1></center>
<hr><center>notginx/0.0.1</center>
</body>
</html>
END
else
	CACHE=cache${FILE##data}.html
	echo "Server: $SERVER_SOFTWARE"
	echo "Content-Type: text/html; charset=UTF-8"
	echo
	if ! [ -e "$CACHE" ] ||
		[ $(stat -c "%Y" $FILE) -gt $(stat -c "%Y" $CACHE) ];then
		pandoc $FILE -s --to html5 -H header.html -A footer.html -o $CACHE
	fi
	cat "$CACHE"
fi

