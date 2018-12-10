import pygame

pygame.init()

import functions

from player import *
from npc import *
from items import *
from container import *
from pausemenu import *
from quest import *
from object_template import *
from map_load import *


# TODO: STUFF TO DO
# TODO: HERE YOU SEE

# BUGS: PROBLEM GOES HERE
#       RECREATION METHOD GOES HERE

class scene:

    def __init__(self):

        self.resolution = (640, 480)
        self.FPS = 30

        self.screen_width = self.resolution[0]
        self.screen_height = self.resolution[1]
        self.screen = pygame.display.set_mode(self.resolution)

        self.GUI = []
        self.render = []
        self.patrol = []
        self.interactable = []
        self.quest = []

        self.init_obj()

        self.objects = []
        self.physical_objects = []

        self.lock = False

        self.activegui = None

        self.pausekey = pygame.K_s
        self.mainkey = pygame.K_a
        self.backkey = pygame.K_b
        self.selectkey = pygame.K_x

    def init_obj(self):
        # objects go here

        self.player = player(self.screen_width / 2, self.screen_height / 2, self.screen)
        self.player.load_sprite("img/student.png")
        self.map1 = JSON_load("Map 2\Map 2.json", self.screen, (self.screen_width, self.screen_height))

        self.init_npc()
        self.init_containers()
        self.init_quest()

        # patrol
        self.patrol.append(None)  # append all NPC that patrol

        # GUI
        self.GUI.append(None)  # append all objects with GUI functionality

        # interactable
        self.interactable.append(None)  # append all objects that are interactable

        # render
        self.render.append(self.player)  # append all objects in the scene for automatic rendering

    def init_npc(self):

        pass  # declare NPC here

    def init_containers(self):

        pass  # declare containers here

    def init_quest(self):

        pass  # declare quests here

    def start(self):

        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.game_loop()

        pygame.quit()
        sys.exit()

    def display(self, obj):

        for obj in self.objects:
            self.screen.blit(obj.sprite, (obj.x, obj.y))

        for obj in self.physical_objects:
            self.screen.blit(obj.sprite, (obj.x, obj.y))

    def event_handler(self, event):

        if event.type == pygame.QUIT:
            self.running = False

        if self.activegui:
            self.activegui.event_handler(event)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:

                pygame.time.set_timer(24, 500)

                if self.activegui:
                    self.activegui.renderdyn = False

                # interacting with GUI
                if not self.lock:

                    instances = []
                    interactable = []
                    for int in self.interactable:

                        if inrange(self.player.rect, int.rect, 50):
                            instances.append(int)

                    interactable = findclosest(self.player, instances)

                    if interactable:
                        interactable.active = True

            elif event.key == pygame.K_s and not self.lock:

                self.pause.active = True

        if not self.lock:
            self.player.set_move(event)

    def GUI_handler(self):

        if self.activegui:

            if not self.activegui.active:  # checks if the GUI is still active and removes it if its not

                self.activegui.guirenderstatic = []
                self.activegui.guirenderdynamic = []

                self.activegui = None
                self.lock = False

            else:

                # checks if the static part is old, then updates the entire GUI
                if self.activegui.lastinit[1] != self.activegui.current[1]:

                    self.activegui.initgui(self.screen_width, self.screen_height)

                # checks if the dynamic part is old, then updates only the dynamic
                elif self.activegui.lastinit[0] != self.activegui.current[0]:

                    self.activegui.initonlydyn()

        else:

            for gui in self.GUI:

                if gui.active:
                    gui.initvars()
                    gui.initgui(self.screen_width, self.screen_height)

                    self.activegui = gui
                    self.lock = True

                    break

    def game_loop(self):

        # logic
        event_list = pygame.event.get()
        for event in event_list:
            self.event_handler(event)

        self.player.move(self.map1)

        # self.GUI_handler()

        for q in self.quest:

            if q.delete:
                self.quest.remove(q)

            q.update()

        for obj in self.objects:
            obj.event_handler()

        for obj in self.physical_objects:
            obj.event_handler()

        # display
        self.map1.update(event_list, self.player)

        self.player.mapCheckMove(self.map1)

        for obj in self.render:  # goes through all objects in the render queue and blits them

            self.screen.blit(obj.sprite, (obj.rect.x, obj.rect.y))

        if self.activegui:
            self.activegui.displaygui(self.screen)

        pygame.display.update()
        self.clock.tick(self.FPS)


scene1 = scene()
scene1.start()
