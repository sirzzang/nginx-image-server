#!/usr/bin/python3
import cgi

form = cgi.FieldStorage()

# request uri에서 image id 추출
image_id = form.getvalue('id')

print("Content-Type: text/html")
print()
print("<h1>delete</h1>")
print(form)
