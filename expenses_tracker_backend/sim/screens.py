"""
Moving across screens:
    Each screen should be instantiated only once,
    so you should make sure that there is only one instance 
    of each.
    You then have to look through the objects defined in the namespace and 
    get a reference to the right screen.
"""


import abc
from expenses_tracker_backend.sim.buttons import *
from expenses_tracker_backend.cls.manager import ProfileManager
class Screen(abc.ABC):
    def __init__(self):
        self.title = ''
        self.reachable_screens = {}
        self.action_buttons = {}
        self.items = {}
        self.manager = Singleton.get_instance(ProfileManager)
        
        # Set by screen that opens this screen
        self.coming_from = None
    
    def __str__(self) -> str:
        return self.title
    
    def __repr__(self) -> str:
        return str(self)
    
    def update_pressables_list(self):
        self.items = {
            group.id : GroupScreen(group) for group in self.manager.user_groups.values()
        }
        self.items.update(
            {list_.id : ListButton(self, list_) for list_ in self.manager.user_lists.values()}
        )
        # For UI purposes
        self.pressables = list(self.reachable_screens.values()) + list(self.action_buttons.values())\
                          + list(self.items.values())
        self.pressables = [(i,pressable) for i,pressable in enumerate(self.pressables)]
        
    def change_screen(self,button_name):
        self.reachable_screens[button_name].open(self)
    
    def open(self, opened_by = None):
        if opened_by:
            self.coming_from = opened_by
        print(f"Opening {self.title}")
        self.display_screen()
    
    def display_screen(self):
        self.update_pressables_list()
        print(self.title)
        print(self.text)
        self.show_pressables()

    def show_pressables(self):
        for i,button in self.pressables:
            print(i,button)
        valid_choice = False
        while not valid_choice:
            try:
                choice = int(input())
                if 0 <= choice < len(self.pressables):
                    valid_choice = True
                else:
                    print("Invalid choice. Choose again.")
            except ValueError:
                print("Inputs are expected to be numbers.")

        chosen_button = type(self.pressables[choice][1])
        self.logger.debug(f"Chosen {chosen_button}")
        print(self.pressables)
        if chosen_button in self.reachable_screens:
            self.change_screen(chosen_button)
        elif chosen_button in self.action_buttons:
            self.action_buttons[chosen_button].pressed()
        else:
            chosen_button = self.pressables[choice][1]
            self.change_screen(chosen_button)
        
    def back_to_previous(self):
        # We don't update 'coming_from' so that it's possible
        # to chain 'backs' and reach the starting screen.
        self.coming_from.open()
    
    def add_screens(self, screens_dict:dict):
        self.reachable_screens.update(screens_dict)
    
    def add_instances_to_dictionaries(self):
        """
        Check if the screens and buttons required by this screen were initialized before.
        If they were, get their singleton instance, otherwise initialize them.
        """
        for screen in self.reachable_screens:
            print(issubclass(screen, Singleton))
            if issubclass(screen, Singleton):
                self.reachable_screens[screen] = screen()
        for button in self.action_buttons:
            if issubclass(button, Singleton):
                self.action_buttons[button] = button(self)

class SettingsScreen(Screen, Singleton):
    def __init__(self):
        super().__init__()
        self.title = 'Settings'
        self.text = "No settings available rn."

class MainScreen(Screen, Singleton):
    def __init__(self):
        super().__init__()
        self.title = 'Main Screen'
        self.text = ''
        self.reachable_screens = {
            SettingsScreen: None,
        }
        self.action_buttons = {
            NewGroupButton: None,
            QuitButton: None
        }
        self.add_instances_to_dictionaries()
        self.update_pressables_list()

class GroupScreen(Screen):
    def __init__(self, group):
        super().__init__()
        self.group = group
        self.text = group.summary()
        self.title =  '{0} ({1})'.format(group.name, group.id)
        self.reachable_screens = {
            MainScreen: None,
        }
        self.action_buttons = {
            BalanceGroupButton: None
        }
        self.add_instances_to_dictionaries()
        self.update_pressables_list()
        

class ListButton(Button):
    def __init__(self, owner, list_: List):
        super().__init__(owner)
        self.list_ = list_
        self.name = '{0} ({1})'.format(list_.name, list_.id)
        self.text = list_.summary()


        



