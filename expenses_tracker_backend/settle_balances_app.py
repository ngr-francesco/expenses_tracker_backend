from expenses_tracker_backend.cls.group import Group
import os
from expenses_tracker_backend.utils.const import default_data_dir
from expenses_tracker_backend.cls.manager import ProfileManager

def display_groups(manager: ProfileManager):
    for idx, group in enumerate(manager.user_groups.values()):
        print(idx, group.name, group.id)

def display_lists(manager: ProfileManager):
    for idx, list_ in enumerate(manager.user_lists.values()):
        print(idx, list_.name, list_.id)

def main_screen(manager):
    print('Groups:')
    display_groups(manager)
    print('Lists:')
    display_lists(manager)

def main():
    manager = ProfileManager(default_data_dir)
    while True:
        
        input()
