import pygame
from OrangeFoxEngine.scenes.base import BaseScene, SwitchObserver


class App(SwitchObserver):
    SCREEN_WIDTH: int = 256
    SCREEN_HEIGHT: int = 224

    def __init__(self, initial_scene: BaseScene, fullscreen: bool = True):
        pygame.init()
        self._fullscreen = fullscreen
        self._switch_scene(initial_scene)

    def run(self):
        flags = pygame.FULLSCREEN if self._fullscreen else 0
        self._screen = pygame.display.set_mode(
            (App.SCREEN_WIDTH, App.SCREEN_HEIGHT), flags=flags
        )

        self._main_loop()

    def _main_loop(self):
        previous = pygame.time.get_ticks()
        lag = 0

        MS_PER_FIXED = 20

        running = True
        while running:
            current = pygame.time.get_ticks()
            elapsed = current - previous
            previous = current
            lag += elapsed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self._current_scene.process_input(event)

            while lag > MS_PER_FIXED:
                self._current_scene.fixed_update()
                lag -= MS_PER_FIXED

            self._current_scene.update()
            self._screen.blit(self._current_scene.render())
            pygame.display.flip()

    def handle_switch(self, current_scene, new_scene):
        current_scene.remove_switch_observer(self)
        self._switch_scene(new_scene)

    def _switch_scene(self, scene: BaseScene):
        self._current_scene: BaseScene = scene
        self._current_scene.add_switch_observer(self)
