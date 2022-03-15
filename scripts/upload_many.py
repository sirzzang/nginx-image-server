#!/usr/bin/python3
import cgi
import cgitb
import os
import sys
import json

cgitb.enable(format="text")

form = cgi.FieldStorage(keep_blank_values=False)

# TODO: 응답 객체 생성 및 응답 상태 코드 utils 분리
resp = {}
resp.setdefault('code', 200)
resp.setdefault('message', '')

# TODO: image key 없을 때 에러 처리
files = [form.getvalue(key) for key in form.keys()]
cnt = len(files)

# 이미지 경로 저장 배열
path_cache = [path for _, _, path in files]

# 이미지 경로 추출
IMAGE_ROOT = 'images'
for i, (file_name, content_type, path) in enumerate(files):

    # 업로드된 파일 중 content type이 이미지가 아닌 것이 있을 때
    if not content_type.startswith('image'):
        for p in path_cache:
            os.remove(p)
        resp['code'] = 400
        resp['message'] = f'content type {content_type} of file {file_name} not allowed.'
        print("Content-Type: application/json")
        print()
        print(json.dumps(resp))
        sys.exit(0)

    hashed_path = path.split(IMAGE_ROOT)[-1]
    image_id = hashed_path.replace('/', '')
    files[i].append(image_id)

# TODO: 응답 객체 생성 및 응답 상태 코드, 메시지 등 정의/ 상태코드 생성 등 utils 분리
resp['message'] = f'{cnt} images successfully uploaded'
resp['data'] = [
    {
        'file_name': file[0],
        'image_id': file[-1]
    } for file in files
]

# 업로드 성공 시 응답 반환
print("Content-Type: application/json")
print()
print(json.dumps(resp))
