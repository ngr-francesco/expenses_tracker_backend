import uuid
from expenses_tracker_backend.expenses_tracker_backend.settings import prefs
from expenses_tracker_backend.cls.saveable import Saveable
import os
import json
class UserProfile:
    def __init__(self,name, usr_id = None):
        super().__init__()
        self.name = name
        self.usr_id = uuid.uuid4() if not usr_id else uuid.UUID(usr_id)
        self.data_dir = prefs.data_dir
        self.local_member_id = None
        self.file_name = str(self.usr_id) + '_usr.json'
    
    @staticmethod
    def load_from_file(path)-> 'UserProfile':
        with open(path,'r') as file:
            data = json.load(file)
        return UserProfile(data['name'], data['usr_id'])
    
    def save(self):
        path = os.path.join(self.data_dir,self.file_name)
        data = {
            'name': self.name,
            'usr_id': str(self.usr_id)
        }
        with open(path,'w+') as file:
            json.dump(data, file)

        
