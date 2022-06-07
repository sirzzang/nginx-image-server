from errors import *


def is_single_file_uploaded(files):
    '''
    Validate if single file has been uploaded by nginx upload module.
    
    Arguments:
        - files {list[str]} -- information of files uploaded via nginx module
    '''
    cnt = len(files)

    if not cnt:
        raise NoFileUploadedError
    elif cnt >= 2:
        raise MultipleFileUploadedError    
    
    return cnt == 1


def are_multiple_files_uploaded(files):
    '''
    Validate if multiple files have been uploaded by nginx upload module.

    Arguments:
        - files {list[str]} -- information of files uploaded via nginx module
    '''
    cnt = len(files)

    if not cnt:
        raise NoFileUploadedError
    elif cnt == 1:
        raise SingleFileUploadedError
    
    return cnt >= 2


def is_valid_file_type(files, allowed_extensions):
    '''
    Validate if file(s) uploaded by nginx module have right types.

    Arguments:
        - files {list[str]} -- information of files uploaded via nginx module
        - allowed_extensions {list[str]} -- allowed extensions for uploading
    '''
    for file in files:
        if not file.endswith(tuple(allowed_extensions)):
            raise NotAllowedExtensionError(file)
    return True
