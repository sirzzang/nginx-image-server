class NoFileUploadedError(Exception):

    def __init__(self):
        super().__init__('No file received.')        


class SingleFileUploadedError(Exception):

    def __init__(self):
        super().__init__('Single file upload not allowed.')


class MultipleFileUploadedError(Exception):

    def __init__(self):
        super().__init__('Multiple file upload not allowed.')


class NotAllowedExtensionError(Exception):

    def __init__(self, file):
        self.file = file
    
    def __str__(self):
        return f'File extension of file {self.file} is not allowed.'


class NoSuchFileError(Exception):

    def __init__(self, file):
        self.file = file

    def __str__(self):
        return f'File {self.file} does not exists.'


class DuplicateFileError(Exception):
    
    def __init__(self, file):
        self.file = file
    
    def __str__(self):
        return f'Duplicate file exists for file_id {self.file}.'