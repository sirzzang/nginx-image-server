#!/usr/bin/env python
import cgitb
import os
import sys
import glob
from urllib.parse import parse_qsl
from response import Response
from utils import delete_from_storage
from errors import NoSuchFileError, DuplicateFileError

# cgi 스크립트 디버깅
cgitb.enable(format="text")

# cgi 스크립트 환경변수
QUERY_STRING = os.getenv("QUERY_STRING")

# 파일 경로 추출
query_dict = dict(parse_qsl(QUERY_STRING))
root_dir = query_dict['type']
file_id = query_dict['id']
dir1 = file_id[0:2]
dir2 = file_id[2:4]
dir3 = file_id[4:6]
dir4 = file_id[6:8]
dir5 = file_id[8:10]
dir6 = file_id[10:12]
file_name = file_id[12:]
file_path = os.path.join("/", root_dir, dir1, dir2, dir3, dir4, dir5, dir6, file_name)

# 파일 삭제
matched_files = glob.glob(f"{file_path}.*")
try:
    temp = delete_from_storage(file_id, matched_files)
except NoSuchFileError as ex:
    '''삭제하고자 하는 파일이 없을 때'''
    resp = Response(400, str(ex))
    resp.send()
    sys.exit(0)
except DuplicateFileError as ex:
    '''삭제하고자 하는 파일이 2개 이상일 때'''
    resp = Response(500, str(ex))
    resp.send()
    sys.exit(0)
else:
    '''성공적으로 삭제했을 때'''
    resp = Response(200, f'File {file_id} successfully deleted.')
    resp.send()
    sys.exit(0)
