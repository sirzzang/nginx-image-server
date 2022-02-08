#!/usr/bin/python3
import cgi
import cgitb
import os
import shutil
import stat

cgitb.enable(display=0, logdir="/home/eraser/nginx/tmp")

form = cgi.FieldStorage(keep_blank_values=True)
path = os.getcwd()
shutil.move('/home/eraser/nginx/tmp/images/0000000014',
            '/home/eraser/images/test2.jpg')


print("Content-Type: text/html")
print()
print("<h1>CGI Temp</h1>")
print(f"<p>path:{path}</p>")
print(f"<p>form:{form}</p>")
