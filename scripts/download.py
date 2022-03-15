#!/usr/bin/python3
import cgi
import cgitb
import imghdr
import json
import os
import sys

cgitb.enable(format="text")

form = cgi.FieldStorage(keep_blank_values=False)

# TODO: 응답 객체 생성 및 응답 상태 코드 utils 분리
resp = {}
resp.setdefault('code', 200)
resp.setdefault('message', '')

# request uri에서 image_id 추출
dir1 = form.getvalue('dir1')
dir2 = form.getvalue('dir2')
dir3 = form.getvalue('dir3')
filename = form.getvalue('filename')

# image_id path 변경
NGINX_ROOT = '/home/eraser/nginx'
IMAGE_ROOT = 'images'
img_path = os.path.join(NGINX_ROOT, IMAGE_ROOT, dir1, dir2, dir3, filename)

# 찾는 이미지가 없을 때
if not os.path.isfile(img_path):
    resp['code'] = 400
    resp['message'] = f'No such image with image_id {dir1}{dir2}{dir3}{filename}'
    print("Content-Type:application/json")
    print()
    print(json.dumps(resp))
    sys.exit(0)

# 이미지 파일 응답
ext = imghdr.what(img_path)  # TODO: svg 형식 확인
content_type = f"Content-Type: image/{ext}\n\n".encode()
with open(img_path, 'rb') as f:
    sys.stdout.buffer.write(content_type)
    sys.stdout.flush()
    sys.stdout.buffer.write(f.read())
