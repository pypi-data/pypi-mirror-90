from abc import ABC

import pygame


class AScene(ABC):
    __slots__ = ("name", "objects")

    def __init__(self, name: str, prev_scene: "AScene" = None) -> None:
        self.name = name
        self.objects = []
        self.prev_scene = prev_scene

    def load(self) -> None:
        # method, in which load all resources
        pass

    def on_scene_change(self) -> None:
        self.objects.clear()

    def on_scene_started(self) -> None:
        self.load()

    def update(self, dt) -> None:
        [o.update(dt) for o in self.objects]

    def draw(self, surface: pygame.Surface) -> None:
        [o.draw(surface) for o in self.objects]

    def handle_events(self, event: pygame.event.Event) -> None:
        [o.handle_events(event) for o in self.objects]
