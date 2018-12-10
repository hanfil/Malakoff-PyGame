# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      filiph
#
# Created:     24.01.2016
# Copyright:   (c) filiph 2016
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# !/usr/bin/env python
import pygame


class Object:
    def __init__(self, x_y, sprite, scene, Map):
        self.x = x_y[0]
        self.y = x_y[1]
        self.sprite = sprite
        self.rect = pygame.Rect(self.x, self.y, self.self.sprite.get_width(), self.sprite.get_height())
        self.scene = scene
        if Map:
            self.map = Map
            self.bg_prevx = self.map.sprite_x
            self.bg_prevy = self.map.sprite_y

        self.scene.objects.append(self)

    def properties(self, physical_object, moving_object, direction, speed, lethal):
        self.physical = physical_object
        self.moving = moving_object
        self.direction = direction
        self.speed = speed
        self.lethal = lethal

        if self.physical:
            self.scene.objects.remove(self)
            self.scene.physical_objects(self)

    def event_handler(self):
        self.Player = self.scene.Player  # It is placed here because the player's properties change everytime it moves

        if self.physical:
            if (((self.Player.x in range(self.x,
                                         self.x + self.width) or self.Player.x + self.Player.sprite_width in range(
                self.x, self.x + self.width)) and  # If Player is in object
                 (self.Player.y in range(self.y,
                                         self.y + self.height) or self.Player.y + self.Player.sprite_height in range(
                     self.y, self.y + self.height))) or  # or if object is in Player
                    ((self.x in range(self.Player.x,
                                      self.Player.x + self.Player.sprite_width) or self.x + self.width in range(
                        self.Player.x, self.Player.x + self.Player.sprite_width)) and
                     (self.y in range(self.Player.y,
                                      self.Player.y + self.Player.sprite_height) or self.y + self.height in range(
                         self.Player.y, self.Player.y + self.Player.sprite_height)))):
                if self.Player.axis == 'x' and self.Player.dir < 0:
                    self.Player.x += self.Player.speed
                elif self.Player.axis == 'x' and self.Player.dir > 0:
                    self.Player.x -= self.Player.speed
                elif self.Player.axis == 'y' and self.Player.dir < 0:
                    self.Player.y += self.Player.speed
                elif self.Player.axis == 'y' and self.Player.dir > 0:
                    self.Player.y -= self.Player.speed

        if self.map:
            if self.bg_prevx < self.map.sprite_x:
                self.x += self.Player.speed
                self.bg_prevx = self.map.sprite_x

            if self.bg_prevx > self.map.sprite_x:
                self.x -= self.Player.speed
                self.bg_prevx = self.map.sprite_x

            if self.bg_prevy < self.scene.sprite_y:
                self.y += self.Player.speed
                self.bg_prevy = self.map.sprite_y

            if self.bg_prevy > self.scene.sprite_y:
                self.y -= self.Player.speed
                self.bg_prevy = self.map.sprite_y

        else:
            x_scaleable = False
            y_scaleable = False
            x__scaleable = False
            y__scaleable = False
            for objects in self.scene.objects:
                if objects.x < 0:
                    x_scaleable = True
                if objects.y < 0:
                    y_scaleable = True
                if objects.rect.right > self.scene.screen_width:
                    x__scaleable = True
                if objects.rect.bottom > self.scene.screen_height:
                    y__scaleable = True
            for objects in self.scene.physical_objects:
                if objects.x < 0:
                    x_scaleable = True
                if objects.y < 0:
                    y_scaleable = True
                if objects.rect.right > self.scene.screen_width:
                    x__scaleable = True
                if objects.rect.bottom > self.scene.screen_height:
                    y__scaleable = True

            if self.Player.x < self.scene.screen_width * (0.25):
                if x_scaleable:
                    for objects in self.scene.objects:
                        objects.x += self.Player.speed
                    for objects in self.scene.physical_objects:
                        objects.x += self.Player.speed

                    self.Player.x -= self.Player.speed

            if self.Player.x > self.scene.screen_width * (0.75):
                if x__scaleable:
                    for objects in self.scene.objects:
                        objects.x -= self.Player.speed
                    for objects in self.scene.physical_objects:
                        objects.x -= self.Player.speed

                    self.Player.x += self.Player.speed

            if self.Player.y < self.scene.screen_height * (0.25):
                if y_scaleable:
                    for objects in self.scene.objects:
                        objects.y += self.Player.speed
                    for objects in self.scene.physical_objects:
                        objects.y += self.Player.speed

                    self.Player.y -= self.Player.speed

            if self.Player.y > self.scene.screen_height * (0.75):
                if y__scaleable:
                    for objects in self.scene.objects:
                        objects.y -= self.Player.speed
                    for objects in self.scene.physical_objects:
                        objects.y -= self.Player.speed

                    self.Player.y += self.Player.speed


class moving_object():
    def __init__(self, x_y, sprite, direction, speed, scene):
        self.x = x_y[0]
        self.y = x_y[1]
        self.sprite = sprite
        self.height = pygame.Surface.get_size(self.sprite)[1]
        self.width = pygame.Surface.get_size(self.sprite)[0]
        self.direction = direction
        self.speed = speed
        self.scene = scene
        self.bg_prevx = self.scene.sprite_x
        self.bg_prevy = self.scene.sprite_y
        self.destroyed = False

    def move_handler(self, objectlist):
        Player = self.scene.Player
        if not self.destroyed:
            if ((Player.x in range(self.x, self.x + self.width) or
                 Player.x + Player.sprite_width + 1 in range(self.x, self.x + self.width)) and
                    (Player.y in range(self.y, self.y + self.height) or
                     Player.y + Player.sprite_height in range(self.y, self.y + self.height))):
                if self.direction == 'right':
                    Player.x += self.speed
                elif self.direction == 'left':
                    Player.x -= self.speed
                elif self.direction == 'down':
                    Player.y += self.speed
                elif self.direction == 'up':
                    Player.y -= self.speed

                if Player.moving:
                    if Player.axis == 'x' and Player.dir < 0:
                        Player.x += Player.speed
                    elif Player.axis == 'x' and Player.dir > 0:
                        Player.x -= Player.speed
                    elif Player.axis == 'y' and Player.dir < 0:
                        Player.y += Player.speed
                    elif Player.axis == 'y' and Player.dir > 0:
                        Player.y -= Player.speed

            if self.direction == 'right':
                self.x += self.speed
            elif self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'down':
                self.y += self.speed
            elif self.direction == 'up':
                self.y -= self.speed

            if self.bg_prevx < self.scene.sprite_x:
                self.x += Player.speed
                self.bg_prevx = self.scene.sprite_x
            if self.bg_prevx > self.scene.sprite_x:
                self.x -= Player.speed
                self.bg_prevx = self.scene.sprite_x
            if self.bg_prevy < self.scene.sprite_y:
                self.y += Player.speed
                self.bg_prevy = self.scene.sprite_y
            if self.bg_prevy > self.scene.sprite_y:
                self.y -= Player.speed
                self.bg_prevy = self.scene.sprite_y

            if (self.x + self.width < self.scene.sprite_x or self.x > self.scene.sprite_width or
                    self.y + self.height < self.scene.sprite_y or self.y > self.scene.sprite_height):
                self.destroyed = True

            for objects in objectlist:
                if ((objects.x in range(self.x, self.x + self.width) or objects.x + objects.width in range(self.x,
                                                                                                           self.x + self.width)) and
                        (objects.y in range(self.y, self.y + self.height) or objects.y + objects.height in range(self.y,
                                                                                                                 self.y + self.height))):
                    self.x = self.scene.screen_width
                    self.y = self.scene.screen_height
                    self.destroyed = True
