# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      filiph
#
# Created:     26.01.2016
# Copyright:   (c) filiph 2016
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# !/usr/bin/env python

# from object_template import*
import json, pygame, sys


class Tile(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.currentx = 0
        self.currenty = 0

    def update(self, direction, mapborder):
        global player
        self.direction = direction
        borderx = mapborder[0]
        bordery = mapborder[1]
        if self.direction == "right" and self.currentx > borderx:
            self.rect.left -= self.speed
            self.currentx -= self.speed
        elif self.direction == "left" and self.currentx < 0:
            self.rect.right += self.speed
            self.currentx += self.speed
        elif self.direction == "up" and self.currenty < 0:
            self.rect.top += self.speed
            self.currenty += self.speed
        elif self.direction == "down" and self.currenty > bordery:
            self.rect.bottom -= self.speed
            self.currenty -= self.speed


# class Player(pygame.sprite.Sprite):
# def __init__(self, image, center):
# pygame.sprite.Sprite.__init__(self)
# self.image = pygame.image.load(image)
# self.rect = self.image.get_rect()
# self.rect.center = center

def event_handler(event_list, direction):
    for event in event_list:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = "right"
            elif event.key == pygame.K_LEFT:
                direction = "left"
            elif event.key == pygame.K_UP:
                direction = "up"
            elif event.key == pygame.K_DOWN:
                direction = "down"
            elif event.key == pygame.K_SPACE:
                direction = "stop"
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mousex = mouse_pos[0]
            mousey = mouse_pos[1]
            if mousex > 380:
                direction = "right"
            elif mousex < 100:
                direction = "left"
            elif mousey < 100:
                direction = "up"
            elif mousey > 220:
                direction = "down"

    return (direction)


class JSON_load:
    def __init__(self, Map, screen, SCREENSIZE):
        self.screen = screen
        global all_layers, mapborder, collision_layers, player, current_layer
        mapfile = open(Map).read()
        mapdict = json.loads(mapfile)

        tilesets = mapdict["tilesets"]
        layers = mapdict["layers"]
        height = mapdict["height"]
        width = mapdict["width"]

        all_tiles_from_sets = []

        for tileset in tilesets:
            tileset_image = pygame.image.load("Map 2/" + tileset["image"])
            imageheight = tileset["imageheight"]
            imagewidth = tileset["imagewidth"]
            tilewidth = tileset["tilewidth"]
            tileheight = tileset["tileheight"]
            for y in range(0, imageheight, tileheight):
                for x in range(0, imagewidth, tilewidth):
                    tile = pygame.Surface((tilewidth, tileheight))
                    tile.blit(tileset_image, (0, 0), (x, y, tilewidth, tileheight))
                    all_tiles_from_sets.append(tile)

        all_layers = []

        initial_map_pos = (0, 0)
        collision_layers = []

        for layer in layers:
            data = layer["data"]
            layerheight = layer["height"]
            layerwidth = layer["width"]
            current_layer = pygame.sprite.Group()
            properties = layer["properties"]
            try:
                collision = properties["collision"]
            except KeyError:
                collision = 0
            collision_layers.append(collision)
            data_pos = 0

            for y in range(0, layerheight):
                for x in range(0, layerwidth):
                    gid = data[data_pos]
                    if gid > 0:
                        tile = Tile(all_tiles_from_sets[gid - 1])
                        tilex = (x * tilewidth) + initial_map_pos[0]
                        tiley = y * tileheight + initial_map_pos[1]
                        tile.rect.topleft = (tilex, tiley)
                        tile.image.set_colorkey((0, 0, 0))
                        current_layer.add(tile)
                    data_pos += 1

            all_layers.append(current_layer)

        self.direction = "stop"
        screen_center = screen.get_rect().center
        # player = Player("boy.png", screen_center)
        self.collide = False
        self.prev_direction = "stop"

        layer_width = layers[0]["width"] * tilesets[0]["tilewidth"]
        layer_height = layers[0]["height"] * tilesets[0]["tileheight"]
        layersize = (layer_width, layer_height)

        mapborderx = SCREENSIZE[0] - layer_width
        mapbordery = SCREENSIZE[1] - layer_height
        mapborder = (mapborderx, mapbordery)

    def update(self, event_list, player):
        global all_layers, mapborder, collision_layers, current_layer
        self.direction = event_handler(event_list, self.direction)

        if self.prev_direction == self.direction and self.collide:
            self.direction = "stop"
        else:
            self.collide = False

        self.screen.fill((0, 0, 0))
        layer_pos = 0
        for layer in all_layers:
            layer.update(self.direction, mapborder)
            layer.draw(self.screen)
            if int(collision_layers[layer_pos]) == 1:
                if pygame.sprite.spritecollideany(player, current_layer):
                    if self.direction != "stop":
                        self.prev_direction = self.direction
                    self.direction = "stop"
                    self.collide = True
            layer_pos += 1
