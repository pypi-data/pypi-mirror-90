import os

import pygame
from pygame.time import Clock

from IslandPy.Scenes.TestScene import TestScene


class RenderWindow:
    def __init__(self, scene_list: list) -> None:
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Render Window")
        self.__screen = pygame.display.set_mode((800, 600))
        self.__clock = Clock()
        self.__done = False
        self.__pause = False
        self.__fps = 60
        self.__current_scene = TestScene(name="test")
        self.__scenes = scene_list
        if len(self.__scenes) < 1:
            self.__done = True
            raise Exception("Please, enter 1 or more scenes")

    def start(self, scene_name: str) -> None:
        self.change_scene(scene_name)
        while not self.__done:
            self.__loop()
        self.__current_scene.on_scene_change()
        pygame.quit()

    def change_scene(self, scene_name: str) -> None:
        scene = [s if s.name == scene_name else None for s in self.__scenes][0]
        if not scene:
            self.__done = True
            raise Exception("Scene not found")
        scene.prev_scene = self.__current_scene
        self.__current_scene.on_scene_change()
        self.__current_scene = scene
        self.__current_scene.on_scene_started()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__done = True
            # if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE:
                #     self.__pause = not self.__pause

            if self.__pause:
                continue

            self.__current_scene.handle_events(event)

    def draw(self) -> None:
        self.__current_scene.draw(self.__screen)

    def update(self, dt) -> None:
        if self.__pause:
            return

        self.__current_scene.update(dt)

    def __loop(self) -> None:
        dt = self.__clock.tick(self.__fps)
        self.__screen.fill((34, 34, 34))
        self.handle_events()
        self.update(dt)
        self.draw()
        pygame.display.flip()
