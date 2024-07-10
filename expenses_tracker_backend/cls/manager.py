from expenses_tracker_backend.expenses_tracker_backend.balance_calculator import BalanceCalculator
from expenses_tracker_backend.expenses_tracker_backend.balance_settler import BalanceSettler
from expenses_tracker_backend.cls.group import Group
from expenses_tracker_backend.cls.list import List
from expenses_tracker_backend.cls.usr_profile import UserProfile
from expenses_tracker_backend.sim.singleton import Singleton
from expenses_tracker_backend.expenses_tracker_backend.settings import prefs
import os

class ProfileManager(Singleton):
    def __init__(self, path: str = None):
        """Initialize the manager.

        The path given at initialization will be set as the
        default data directory in the preferences to the application

        Args:
            path (str): the path to load from and save to
        """
        if path is not None:
            prefs.set_data_dir(path= path)
        self.user_profile = self.load_usr()
        self.user_groups = self.load_user_groups()
        self.user_lists = self.load_user_lists()
    
    def rename_usr(self, name):
        self.user_profile.name = name
        self.user_profile.save()

    def load_usr(self):
        file_path = [f for f in os.listdir(prefs.data_dir) if f.endswith('_usr.json')]
        if not len(file_path):
            user = UserProfile('user')
            user.save()
            return user
        if len(file_path)> 1:
            raise ValueError(f"Cannot have more than one user per user directory. {prefs.data_dir}")
        file_path = os.path.join(prefs.data_dir, file_path[0])

        return UserProfile.load_from_file(file_path)

    def load_user_groups(self):
        if not os.path.exists(prefs.data_dir):
            return {}
        groups = {}
        for file in os.listdir(prefs.data_dir):
            if 'Group' in file:
                group_folder = os.path.join(prefs.data_dir, file)
                group_file = [f for f in os.listdir(group_folder) if f.endswith('group_info.json')][0]
                group_file = os.path.join(group_folder, group_file)
                group = Group.load_from_file(group_file)
                groups[group.id] = group
        return groups
    
    def add_user_group(self, group: Group):
        if group.id in self.user_groups:
            raise KeyError(f"Group {group.id} already present for this user")
        self.user_groups[group.id] = group
    
    def add_user_list(self, list_: List):
        if list_.id in self.user_lists:
            raise KeyError(f"List {list_.id} already present for this user")
        self.user_groups[list_.id] = list_

    def load_user_lists(self):
        if not os.path.exists(prefs.ungrouped_lists_dir()):
            return {}
        lists = {}
        for file in os.listdir(prefs.ungrouped_lists_dir()):
            if 'list_info' in file:
                list_file = os.path.join(prefs.data_dir, file)
                list_ = List.load_from_file(list_file)
                lists[list_.id] = list_
        return lists 

    def settle_balances(self, id):
        """
        Find the optimal transactions between group members to settle up 
        a group or list balance. If for group remind the user that they
        are balancing across multiple lists.
        """
        members = self.user_groups[id].members
        bal_settler = BalanceSettler(members, prefs.data_dir)
        bal_settler.generate_settle_up_transactions()
        bal_settler.save_transaction_record(verbose=True)

