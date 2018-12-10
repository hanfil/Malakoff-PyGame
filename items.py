import pygame


class item:
    _list = []

    def __init__(self, name="base_item",
                 sprite="img/base_sprite.png",
                 description="BASECLASS"):
        item._list.append(self)

        self.name = name
        self.thumb = pygame.image.load(sprite)
        self.description = description
