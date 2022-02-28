#!/usr/bin/python3
import cgi
import os
import json

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

# TODO: 응답 객체 생성 및 응답 상태 코드, 메시지 정의 등 utils 분리
resp = {}

# 파일이 존재하면 삭제
is_img_exists = os.path.exists(img_path)
if is_img_exists:
    os.remove(img_path)
    resp['code'] = 200
    resp['message'] = f'image {dir1}{dir2}{dir3}{filename} successfully deleted'
else:
    resp['code'] = 400
    resp['message'] = f'No image with image_id {dir1}{dir2}{dir3}{filename}'

print("Content-Type: application/json")
print()
print(json.dumps(resp))
