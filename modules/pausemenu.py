import pygame
from modules import functions


class pausemenu:
    # GUI
    guirenderstatic = []
    guirenderdynamic = []

    # sprites
    buttonsprite = pygame.image.load('img/pausemenu_button.png')
    selectedprite = pygame.image.load('img/pausemenu_buttonsel.png')

    # font
    textsize = 16
    font = pygame.font.Font('./modules/munro.ttf', textsize)
    textcolour = (50, 50, 75)

    def __init__(self, inv):

        self.active = False
        self.renderdyn = False

        self.buttons = ['Inventory', 'Quit']
        self.curbut = 0
        self.buttonx = None
        self.buttony = None

        self.lastinit = (0, 0)
        self.current = (0, 0)

        self.inventory = inv

    def initvars(self):
        '''resets variables'''

        self.curbut = 0

    def initgui(self, screen_width, screen_height):
        '''updates the GUI'''

        pausemenu.guirenderstatic = []
        pausemenu.guirenderdynamic = []

        self.lastinit = (self.curbut, 0)

        if not self.buttonx:
            self.buttonx = screen_width - pausemenu.buttonsprite.get_width()
            self.buttony = screen_height / 2 - (pausemenu.buttonsprite.get_height() * len(self.buttons)) / 2

        buttonx = self.buttonx
        buttony = self.buttony

        i = 0
        for but in self.buttons:

            if i == self.curbut:

                pausemenu.guirenderdynamic.append((pausemenu.selectedprite, (buttonx, buttony)))

            else:

                pausemenu.guirenderdynamic.append((pausemenu.buttonsprite, (buttonx, buttony)))

            text = pausemenu.font.render(but, 1, pausemenu.textcolour)

            textx = buttonx + pausemenu.buttonsprite.get_width() / 2 - text.get_width() / 2
            texty = buttony + pausemenu.buttonsprite.get_height() / 2 - text.get_height() / 2

            pausemenu.guirenderstatic.append((text, (textx, texty)))

            buttony += pausemenu.buttonsprite.get_height()
            i += 1

    def initonlydyn(self):
        '''updates parts of the GUI'''

        pausemenu.guirenderdynamic = []

        self.lastinit = (self.curbut, 0)

        buttonx = self.buttonx
        buttony = self.buttony

        for i in xrange(len(self.buttons)):

            if i == self.curbut:

                pausemenu.guirenderdynamic.append((pausemenu.selectedprite, (buttonx, buttony)))

            else:

                pausemenu.guirenderdynamic.append((pausemenu.buttonsprite, (buttonx, buttony)))

            buttony += pausemenu.buttonsprite.get_height()

    def displaygui(self, screen):
        '''renders the GUI'''

        for obj in pausemenu.guirenderdynamic:
            screen.blit(obj[0], obj[1])

        for obj in pausemenu.guirenderstatic:
            screen.blit(obj[0], obj[1])

    def event_handler(self, event):
        '''keyboard input'''

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN and self.curbut + 1 < len(self.buttons):

                self.curbut += 1

            elif event.key == pygame.K_UP and self.curbut > 0:

                self.curbut -= 1

            elif event.key == pygame.K_a:

                but = self.buttons[self.curbut]

                if but == 'Inventory':

                    self.inventory.active = True
                    self.active = False

                elif but == 'Quit':

                    pygame.quit()

            elif event.key == pygame.K_b:

                self.active = False
        self.current = (self.curbut, 0)
