#!/usr/bin/python3
import cgi
import cgitb
import imghdr
import os
import sys

cgitb.enable(format="text")

form = cgi.FieldStorage()

# request uri에서 image id 추출
# TODO: image_id 없거나, image_id 형식 잘못되었을 때 400에러
dir1 = form.getvalue('dir1')
dir2 = form.getvalue('dir2')
dir3 = form.getvalue('dir3')
filename = form.getvalue('filename')

# TODO: path 변경
NGINX_ROOT = '/home/eraser/nginx'
IMAGE_ROOT = 'images'
img_path = os.path.join(NGINX_ROOT, IMAGE_ROOT, dir1, dir2, dir3, filename)

# content-type 헤더
ext = imghdr.what(img_path)  # TODO: svg 형식 확인
content_type = f"Content-Type: image/{ext}\n\n".encode()

# 이미지 파일 응답
with open(img_path, 'rb') as f:
    # sys.stdout.buffer.write(b"Content-Type: image/gif\n\n")
    sys.stdout.buffer.write(content_type)
    sys.stdout.flush()
    sys.stdout.buffer.write(f.read())
