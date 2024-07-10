import abc
import sys
from expenses_tracker_backend.sim.singleton import Singleton
from expenses_tracker_backend.cls.group import Group
from expenses_tracker_backend.cls.list import List
from expenses_tracker_backend.cls.manager import ProfileManager
class Button(abc.ABC):
    def __init__(self, owner):
        self.owner = owner
        self.name = ''
        self.text = ''
        self.input_fields = {}
        self.screen_after_pressed = None
        self.manager = Singleton.get_instance(ProfileManager) 
    
    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return str(self)
    
    def pressed(self, *args):
        print(self.text)
        if len(self.input_fields):
            for field in self.input_fields:
                self.input_fields[field] = input(field+ ': ')

class QuitButton(Button, Singleton):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Quit'
        self.text = 'Exiting application ...'
        self.screen_after_pressed = None
    
    def pressed(self, *args):
        super().pressed(*args)
        input()
        sys.exit()

class NewGroupButton(Button, Singleton):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'New Group'
        self.text = 'Insert group name'
        self.input_fields = {
            'name': None
        }
    
    def pressed(self, *args):
        super().pressed(*args)
        # --- Insert functionality here:
        name = self.input_fields['name']
        group = Group(name= name)
        self.manager.add_user_group(group)
        print(self.manager.user_groups)
        # -----------------------------
        if self.owner:
            self.owner.display_screen()

class BalanceGroupButton(Button):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Generate settle-up transactions"
        self.text = "Balancing group expenses .."
    
    def pressed(self, *args):
        super().pressed(*args)
        self.manager.settle_balances(self.owner.group.id)
