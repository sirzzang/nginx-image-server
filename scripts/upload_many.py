#!/usr/bin/python3
import cgi
import cgitb
import json

# cgi 스크립트 에러 핸들링
cgitb.enable(format="text")

form = cgi.FieldStorage(keep_blank_values=False)

# TODO: image key 없을 때 에러 처리
files = [form.getvalue(key) for key in form.keys()]
cnt = len(files)

# 이미지 id 추출: hashed_path + ext
for i, (file_name, content_type, path) in enumerate(files):
    IMAGE_URL = '/images/'
    hashed_path = path.split(IMAGE_URL)[-1]
    image_id = hashed_path.replace('/', '')
    files[i][2] = image_id

# TODO: 응답 해시값 암호화, 이미지 url 분리, utils 분리


# TODO: 확장자 검증, 미디어 타입 검증, validator 혹은 utils 분리

# TODO: 응답 객체 생성 및 응답 상태 코드, 메시지 등 정의/ 상태코드 생성 등 utils 분리
resp = {}
resp['code'] = 200
resp['message'] = f'{cnt} images upload successfully done'
resp['data'] = {}
resp['data']['cnt'] = cnt
resp['data']['image_ids'] = [
    {
        'file_name': file[0],
        'image_id': file[2]
    } for file in files
]
resp_json = json.dumps(resp)

# TODO: cgi 스크립트 오류 시 처리(cleanup, 에러 코드 세분화)
print("Content-Type: application/json")
print()
print(json.dumps(resp))
