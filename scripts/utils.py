import os
import uuid
import shutil
from errors import NoSuchFileError, DuplicateFileError


def generate_uuid():
    '''
    Generate uuid for processing files uploaded from nginx module.
    
    Returns:
        randomly generated uuid
    '''
    return str(uuid.uuid4())


def generate_path(uuid, root_dir, path_threshold=12, path_step=2):
    '''
    Generate new path structure using uuid for files uploaded by nginx module.
    
    Arguments:
        - uuid {str} -- uuid used for generating directory structure
        - root_dir {str} -- root directory for the uploaded file to be stored
        - path_threshold {int} -- threshold index for generating path structure
        - path_step {int} -- step interval for generating path structure

    Returns:
        - new_dir {str} -- path-like string. newly generated directory using uuid
        - new_name {str} -- newly generated file name using uuid
    '''

    # subdirectory structure
    dir = uuid[:path_threshold]
    sub_dir = "/".join([
        dir[i : i+path_step] for i in range(0, path_threshold, path_step)
    ])
    new_dir = os.path.join(root_dir, sub_dir)
    
    # file name
    new_name = uuid[path_threshold:]

    return new_dir, new_name


def move_file(src_path, dst_path):
    '''
    Move file.

    Arguments:
        - src_path {str} -- source file path
        - dst_path {str} -- destination file path
    '''
    shutil.move(src_path, dst_path)


def move_upload_to_storage(file, root_dir):
    '''
    Move uploaded files from nginx module to storage.
    
    Arguments:
        - file {list[str]} -- information of file uploaded via nginx module
            - file_name -- name of uploaded file
            - content_type -- HTTP content_type of uploaded file
            - path -- temporary path of uploaded file
        - root_dir {str} -- root directory for the uploaded file to be stored

    Returns:
        - file_name {str} -- name of uploaded file via nginx module
        - uuid_processed {str} -- id of uploaded file via media service
    '''

    # uploaded file info
    file_name, _, path = file
    _, ext = os.path.splitext(file_name)

    # generate uuid
    uuid = generate_uuid()
    uuid_processed = uuid.replace("-", "")

    # generate directory structure for new path
    new_dir, new_name = generate_path(uuid_processed, root_dir)

    # make new_dir recursively if it does not exists
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    
    # move file to new path
    new_path = os.path.join(new_dir, new_name + ext)
    move_file(path, new_path)

    return file_name, uuid_processed


def rollback_upload(paths):
    '''
    Delete uploaded files from nginx module when upload request is invalid.
    
    Arguments:
        - paths {list[str]} -- temporary paths of uploaded files via nginx module
    '''
    for path in paths:
        os.remove(path)


def delete_from_storage(file_id, paths):
    '''
    Delete files from media service storage when user requests.

    Arguments:
        - file_id {str} -- id of file to be deleted
        - paths {list[str]} -- file paths matched with requested file_id
    '''
    if not paths:
        raise NoSuchFileError(file_id)
    elif len(paths) >= 2:
        raise DuplicateFileError(file_id)
    else:
        os.remove(paths[0])
