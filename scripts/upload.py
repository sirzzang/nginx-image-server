#!/usr/bin/python3
import json
import cgitb
import cgi

# cgi 스크립트 에러 핸들링
cgitb.enable(format="text")

form = cgi.FieldStorage(keep_blank_values=False)

# TODO: image key 없을 때 에러 처리
file_name = form.getvalue("file_name")
content_type = form.getvalue("content_type")
path = form.getvalue("path")

# 이미지 id 추출: hashed_path + ext
IMAGE_ROOT = 'images'
hashed_path = path.split(IMAGE_ROOT)[-1]
image_id = hashed_path.replace('/', '')

# TODO: 응답 객체 생성 및 응답 상태 코드, 메시지 정의 등 utils 분리
resp = {}
resp['code'] = 200
resp['message'] = 'image successfully uploaded'
resp['data'] = {}
resp['data']['file_name'] = file_name
resp['data']['image_id'] = image_id
resp_json = json.dumps(resp)

# TODO: cgi 스크립트 오류 시 처리(cleanup, 에러 코드 세분화)
print("Content-Type: application/json")
print()
print(json.dumps(resp))
