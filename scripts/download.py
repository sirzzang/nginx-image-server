#!/usr/bin/python3
import cgi
import cgitb
import imghdr

cgitb.enable(format="text")

form = cgi.FieldStorage()

# request uri에서 image id 추출
dir1 = form.getvalue('dir1')
dir2 = form.getvalue('dir2')
dir3 = form.getvalue('dir3')
filename = form.getvalue('filename')

# ext = imghdr.what(f"/home/eraser/nginx/images/{dir1}/{dir2}/{dir3}/{filename}")

print("Content-Type: text/html")
print()
print("<h1>download</h1>")
print(form)
# print(ext)

'''
# import imghdr

# ext = imghdr.what('/home/eraser/nginx/images/59/71/19/0035197159')


# # TODO: cgi 스크립트 오류 시 처리(cleanup, 에러 코드 세분화)
# print("Content-Type: text/html")
# print()
# print(ext)

#!/usr/bin/python3
import cgi
import cgitb
import json

# cgi 스크립트 에러 핸들링
cgitb.enable(format="text")

form = cgi.FieldStorage(keep_blank_values=False)

# TODO: image key 없을 때 에러 처리

file_name = form.getvalue("file_name")
content_type = form.getvalue("content_type")
path = form.getvalue("path")

# 이미지 id 추출: hashed_path + ext
ext = content_type.split('/')[-1]
IMAGE_URL = '/images/'
hashed_path = path.split(IMAGE_URL)[-1]
image_id = hashed_path.replace('/', '')

# TODO: 응답 해시값 암호화, 이미지 url 분리, utils 분리

# TODO: 확장자 검증, 미디어 타입 검증, validator 혹은 utils 분리

# TODO: 응답 객체 생성 및 응답 상태 코드, 메시지 등 정의/ 상태코드 생성 등 utils 분리
resp = {}
resp['code'] = 200
resp['message'] = 'image upload successfully done'
resp['data'] = {}
resp['data']['file_name'] = file_name
resp['data']['image_id'] = image_id
resp_json = json.dumps(resp)

# TODO: cgi 스크립트 오류 시 처리(cleanup, 에러 코드 세분화)
print("Content-Type: application/json")
print()
print(json.dumps(resp))
'''
