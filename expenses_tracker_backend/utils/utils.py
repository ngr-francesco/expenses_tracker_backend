from typing import Any
from expenses_tracker_backend.cls.saveable import Saveable
from dataclasses import dataclass
from expenses_tracker_backend.settings import prefs
from expenses_tracker_backend.utils.ids import IdFactory
import os, shutil

def reload_backend():
    """
    Save and reload all instances of Saveable
    """
    for instance in Saveable._instances:
        instance.save_data()
        instance.load()

def save_all():
    """
    Save all saveable objects
    """
    for instance in Saveable._instances:
        instance.save_data()

def remove_data_and_reset():
    try:
        shutil.rmtree(prefs.data_dir)
        IdFactory.hard_reset()
    except FileNotFoundError:
        pass

