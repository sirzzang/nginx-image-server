#!/usr/bin/python3
import json
import cgitb
import cgi
import sys
import os

# cgi 스크립트 에러 핸들링
cgitb.enable(format="text")

form = cgi.FieldStorage(keep_blank_values=False)

# TODO: 응답 객체 생성 및 응답 상태 코드 utils 분리
resp = {}
resp.setdefault('code', 200)
resp.setdefault('message', '')

# 업로드한 파일
file_name = form.getvalue("file_name")
content_type = form.getvalue("content_type")
path = form.getvalue("path")

# 업로드 파일의 content type이 이미지가 아닐 때 예외 처리
if not content_type.startswith('image'):
    os.remove(path)
    resp['code'] = 400
    resp['message'] = f'content type {content_type} of fie {file_name} not allowed.'
    print("Content-Type: application/json")
    print()
    print(json.dumps(resp))
    sys.exit(0)


# 이미지 id 추출: hashed_path + ext
IMAGE_ROOT = 'images'
hashed_path = path.split(IMAGE_ROOT)[-1]
image_id = hashed_path.replace('/', '')

# TODO: 응답 객체 생성 및 응답 상태 코드, 메시지 정의 등 utils 분리
resp = {}
resp['message'] = 'image successfully uploaded'
resp['data'] = {}
resp['data']['file_name'] = file_name
resp['data']['image_id'] = image_id
resp_json = json.dumps(resp)

# 업로드 성공 시 응답 반환
print("Content-Type: application/json")
print()
print(json.dumps(resp))
