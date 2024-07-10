from expenses_tracker_backend.utils.const import default_data_dir
import os

class Settings:
    data_dir = default_data_dir

    def set_data_dir(path):
        if os.path.isdir(path):
            Settings.data_dir = os.path.join(path,'usr_data')
    
    @classmethod
    def ungrouped_lists_dir(cls):
        return os.path.join(cls.data_dir, 'ungrouped_lists')

prefs = Settings
