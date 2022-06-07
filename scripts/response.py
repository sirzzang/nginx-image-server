import json


class Response:
    
    def __init__(self, code, message):
        self.code = code
        self.message = message
        
    def build(self, key, value):
        self.__setattr__(key, value)
        
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def send(self):
        print("Content-Type: application/json")
        print()
        print(self.to_json())
