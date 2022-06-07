#!/usr/bin/env python
import cgi
import cgitb
import os
import sys
from response import Response
from utils import move_upload_to_storage, rollback_upload
from validate import is_single_file_uploaded, is_valid_file_type
from errors import NoFileUploadedError, MultipleFileUploadedError, NotAllowedExtensionError

# cgi 스크립트 디버깅
cgitb.enable(format="text")

# cgi 스크립트 form 및 환경변수
form = cgi.FieldStorage(keep_blank_values=False)
UPLOAD_DUMMY_CODE = os.getenv('UPLOAD_DUMMY_CODE')
ALLOWED_IMG = os.getenv('ALLOWED_IMG')
REQUEST_URI = os.getenv('REQUEST_URI')
UPLOAD_ROOT = os.getenv('UPLOAD_ROOT')

# upload 처리를 위한 변수
allowed_images = ALLOWED_IMG.split(',')
root_dir = REQUEST_URI.split(UPLOAD_ROOT)[0]

# 업로드한 파일
files = [form.getvalue(key) for key in form.keys() if key != UPLOAD_DUMMY_CODE]

# 파일 개수 검증
try:
    is_single_file_uploaded(files)
except NoFileUploadedError as ex:
    '''
    업로드된 파일이 없는 경우
        1. Body가 비어 있는 경우, Content-Type 헤더가 없어 Nginx 단에서 400 Bad Request 처리
        2. Body가 있으나 File type이 아닌 경우, 아래 부분에서 400 에러 처리
    '''
    resp = Response(400, str(ex))
    resp.send()
    sys.exit(0)
except MultipleFileUploadedError as ex:
    '''여러 개의 파일이 업로드된 경우'''
    resp = Response(400, str(ex))
    resp.send()
    sys.exit(0)
else:
    file_names = [name for name, _, _ in files if files]
    file_paths = [path for _, _, path in files if files]

# 확장자 검증
try:
    is_valid_file_type(file_names, allowed_images)
except NotAllowedExtensionError as ex:
    rollback_upload(file_paths)
    resp = Response(400, str(ex))
    resp.send()
    sys.exit(0)
    
# uuid 발급 후 업로드 처리
data = {}
try:
    file_name, file_id = move_upload_to_storage(files[0], root_dir)
except:
    pass
else:
    data['file_name'] = file_name
    data['file_id'] = file_id

# 업로드 성공 시 응답 반환
resp = Response(200, 'File(s) successfully uploaded.')
resp.build("data", data)
resp.send()
sys.exit(0)
