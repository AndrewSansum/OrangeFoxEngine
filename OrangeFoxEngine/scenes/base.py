from abc import ABC, abstractmethod
import pygame


class SwitchObserver(ABC):
    @abstractmethod
    def handle_switch(self, current_scene, new_scene):
        pass


class BaseScene(ABC):
    def __init__(self, width: int, height: int):
        self._surface = pygame.Surface((width, height))
        self._switch_observers: set[SwitchObserver] = set()

    def add_switch_observer(self, ob: SwitchObserver):
        self._switch_observers.add(ob)

    def remove_switch_observer(self, ob: SwitchObserver):
        try:
            self._switch_observers.remove(ob)
        except KeyError:
            return

    def notify_switch_observers(self, new_scene):
        for ob in self._switch_observers.copy():
            ob.handle_switch(self, new_scene)

    @abstractmethod
    def process_input(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def fixed_update(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self) -> pygame.Surface:
        pass
