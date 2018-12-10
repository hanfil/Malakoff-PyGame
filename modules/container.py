import pygame
from modules import playerstats
from modules.functions import *
# keeps control of items and has a GUI for navigating through them
class container:
    '''holds items'''

    # GUI
    current = [0, 0]
    lastinit = [0, 0]
    guirenderstatic = []
    guirenderdynamic = []

    # font
    textsize = 15
    font = pygame.font.Font('./modules/munro.ttf', textsize)
    textcolour = (204, 0, 0)

    def __init__(self, x_y, sprite, inventory=False, physical=True):

        if physical:
            x, y = x_y
            self.sprite = pygame.image.load(sprite)
            self.rect = pygame.Rect(x, y, self.sprite.get_width(), self.sprite.get_height())

        self.active = False
        self.inventory = inventory
        self.pause = None

        self.maxcol = 5
        self.maxrow = 3
        self.maxsel = None
        self.maxpage = 0

        self.startingrect = None
        self.currentsel = [1, 1]
        self.selected = None
        self.currentpage = 0

        self.numbers = []
        for i in range(3):
            self.numbers.append(pygame.image.load("img/wood".split('_')[0] + '_' + str(i+1) + '.png'))
        self.sprite_bg = pygame.image.load("img/rect_bg.png")
        self.sprite_item = pygame.image.load("img/rect_item.png")
        self.sprite_selected = pygame.image.load("img/rect_selected.png")
        self.descbg = pygame.image.load("img/container_descbg.png")
        self.bg = None
        self.renderdyn = False

        self.items = []
        self.pages = []

    def displaygui(self, screen):
        '''rendering'''

        if self.items:

            if not self.selected:

                self.selected = (self.sprite_selected, self.startingrect)

        else:

            self.selected = (self.sprite_selected, (-400, -400))

        screen.blit(self.bg[0], self.bg[1])

        for obj in self.guirenderstatic:
            screen.blit(obj[0], obj[1])

        for item in self.pages[self.currentpage]:

            screen.blit(item[0], item[1])

        screen.blit(self.selected[0], self.selected[1])

    def add(self, obj):
        '''adding items'''

        new = True

        if new:

            self.items.append(obj)

    def rem(self, obj):
        '''removing items'''

        self.items.remove(obj)

    def event_handler(self, event):
        '''keyboard input'''

        if event.type == pygame.KEYDOWN:

            if self.pages:

                self.maxsel= len(self.pages[self.currentpage]) / 2
                cursel = self.currentsel[0] + (self.maxcol * (self.currentsel[1]-1))

                if event.key == pygame.K_RIGHT:

                    container.lastinit = [0, 99]

                    if cursel < self.maxsel:

                        self.currentsel[0] += 1

                        if self.currentsel[0] > self.maxcol:

                                self.currentsel[0] = 1
                                self.currentsel[1] += 1

                    elif self.currentpage < self.maxpage:

                        self.currentsel = [1, 1]
                        self.currentpage += 1

                elif event.key == pygame.K_LEFT:

                    container.lastinit = [0, 99]

                    if cursel > 1:

                            self.currentsel[0] -= 1

                            if self.currentsel[0] == 0:

                                if self.currentsel[1] > 1:

                                    self.currentsel[0] = self.maxcol
                                    self.currentsel[1] -= 1

                    elif self.currentpage > 0:

                        self.currentsel[0] = self.maxcol
                        self.currentsel[1] = self.maxrow
                        self.currentpage -= 1

                elif event.key == pygame.K_UP:

                    container.lastinit = [0, 99]

                    if self.currentsel[1] > 1:

                        self.currentsel[1] -= 1

                    elif self.currentpage > 0:

                        self.currentpage -= 1
                        self.currentsel[1] = self.maxrow

                elif event.key == pygame.K_DOWN:

                    container.lastinit = [0, 99]

                    if cursel+self.maxcol-1 < self.maxsel:

                        self.currentsel[1] += 1

                    elif self.currentpage != self.maxpage:

                        self.currentpage += 1
                        self.currentsel[0] = 1
                        self.currentsel[1] = 1

                elif event.key == pygame.K_a:

                    self.lastinit = [0, 99]

                    if self.items:

                        if not self.inventory:

                            item = self.items[self.currentsel[0]-1 + (self.maxcol * (self.currentsel[1]-1)) + ((self.maxcol * self.maxrow) * (self.currentpage))]
                            playerstats.items.append(item)
                            self.items.remove(item)

                            try:

                                self.items[self.currentsel[0]-1 + (self.maxcol * (self.currentsel[1]-1)) + ((self.maxcol * self.maxrow) * (self.currentpage))]

                            except IndexError:

                                if self.currentsel == [1, 1]:

                                    if self.currentpage == 0:

                                        self.active = False

                                    else:
                                        self.currentpage -= 1
                                        self.currentsel[0] = self.maxcol
                                        self.currentsel[1] = self.maxrow

                                elif self.currentsel[0] > 1:

                                    self.currentsel[0] -= 1

                                else:

                                    self.currentsel[1] -= 1
                                    self.currentsel[0] = self.maxcol

                            self.initgui(self.screen_width, self.screen_height)

            if event.key == pygame.K_b:

                self.active = False

                if self.inventory:

                    self.pause.active = True

    def initgui(self, screen_width, screen_height):
        '''updating the GUI'''

        container.lastinit = [0, 0]

        self.guirenderstatic = []
        self.guirenderdynamic = []

        if self.inventory:

            self.items = playerstats.items

        if self.pages and len(self.items):

            if self.pages[self.currentpage]:

                item = self.items[self.currentsel[0]-1 + (self.maxcol * (self.currentsel[1]-1)) + ((self.maxcol * self.maxrow) * (self.currentpage))]

            else:

                item = self.items[-1]

        else:

            if len(self.items):

                item = self.items[self.currentsel[0]-1 + (self.maxcol * (self.currentsel[1]-1)) + ((self.maxcol * self.maxrow) * (self.currentpage))]

            else:

                item = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        top_x = (screen_width/2) - (self.sprite_bg.get_width()/2)
        top_y = (screen_height/2) - (self.sprite_bg.get_height()/2)

        rec_x = top_x + self.sprite_item.get_width() / 1.3
        rec_y = top_y + self.sprite_item.get_height() / 2
        self.startingrect = (rec_x, rec_y)
        column = 0
        row = 1
        templist = []
        self.maxpage = 0
        self.pages = []

        self.bg = (self.sprite_bg, (top_x, top_y))

        selrec_x = self.startingrect[0] + (self.sprite_item.get_width() * 1.5) * (self.currentsel[0]-1)
        selrec_y = self.startingrect[1] + (self.sprite_item.get_height() * 1.5) * (self.currentsel[1]-1)

        self.selected = (self.sprite_selected, (selrec_x, selrec_y))

        for currentitem in self.items:

            column += 1

            if len(templist)/2 > self.maxcol * self.maxrow - 1:
                self.pages.append(templist)
                self.maxpage += 1
                templist = []

                rec_x = top_x + self.sprite_item.get_width() / 1.3
                rec_y = top_y + self.sprite_item.get_height() / 2
                column = 1
                row = 1

            if column > 1:
                rec_x += self.sprite_item.get_width() * 1.5

            if column > self.maxcol:

                row += 1
                column = 1

                rec_x = top_x + self.sprite_item.get_width() / 1.3
                rec_y += self.sprite_item.get_height() * 1.5

            templist.append((self.sprite_item, (rec_x, rec_y)))
            templist.append((currentitem.thumb, (rec_x, rec_y)))

        pagex = self.bg[1][0] + self.bg[0].get_width()/2
        pagey = self.bg[1][1] + self.bg[0].get_height()-self.numbers[0].get_height()*2
        self.guirenderstatic.append((self.numbers[self.currentpage], (pagex, pagey)))

        if item:

            currentitemdisplayx = self.bg[1][0] + 40
            currentitemdisplayy = pagey - 4

            self.guirenderstatic.append((self.sprite_item, (currentitemdisplayx, currentitemdisplayy)))
            self.guirenderstatic.append((item.thumb, (currentitemdisplayx, currentitemdisplayy)))

            descbgx = currentitemdisplayx + self.sprite_item.get_width()*1.3 - 12
            descbgy = currentitemdisplayy

            self.guirenderstatic.append((self.descbg, (descbgx, currentitemdisplayy)))

            texty = descbgy + 20
            textx = descbgx + self.descbg.get_width() / 2

            for str in wrap_multi_line(item.description, self.font, 124):

                txt = self.font.render(str, 1, self.textcolour)

                self.guirenderstatic.append([txt, (textx - txt.get_width() / 2, texty)])
                texty += txt.get_height() / 1.5

            name = container.font.render(item.name, 1, container.textcolour)
            namex = descbgx + self.descbg.get_width() / 2 - name.get_width() / 2

            self.guirenderstatic.append((name, (namex, currentitemdisplayy)))

        self.pages.append(templist)
        if self.maxpage > 2:
            self.maxpage = 2

    def initvars(self):
        '''resets variables'''

        self.currentsel = [1, 1]
