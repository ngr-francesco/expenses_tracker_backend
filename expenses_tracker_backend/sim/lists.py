from expenses_tracker_backend.sim.singleton import Singleton
import abc

class List(abc.ABC, Singleton):
    def __init__(self, elements: list):
        self.elements = elements
        