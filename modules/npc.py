import pygame
from math import ceil
from modules.functions import *


# examples
# npc = npc((x, y), spritepath, headpath, dialogue=True)
# npc = npc((x, y), spritepath, patrol=True, speed=3)
# npc = npc((x, y), spritepath) for a dialogueless and unpatrolling npc

# npc.adddialogue('name',
#                 'text',
#                 'answer1', 'answer1_goto'
#                 'answer2', 'answer2_goto')

# npc.addpatrol(x, y)

class dialogue:

    def __init__(self, name, text):
        self.name = name
        self.text = text

        self.answers = []
        self.answers_goto = []


class event:

    def __init__(self, host, dialogue, answer, type):
        self.host = host
        self.name = dialogue
        self.answer = answer
        self.type = type


class npc:
    # sprites
    sprite_bg = pygame.image.load('img/dialogue_bg.png')
    sprite_answer = pygame.image.load('img/dialogue_answer.png')
    sprite_answersel = pygame.image.load('img/dialogue_answersel.png')
    sprite_headframe = pygame.image.load('img/headframe.png')

    # font
    textsize = 20
    font = pygame.font.Font('./modules/munro.ttf', textsize)
    textcolour = (255, 255, 255)

    # GUI
    guirenderstatic = []
    guirenderdynamic = []
    initiated = False
    head_x = None
    head_y = None
    text_x = None
    text_y = None
    answer_x = None
    answer_y = None
    currentdiag = 0
    currentans = 0
    bg = pygame.Rect(0, 0, sprite_bg.get_width(), sprite_bg.get_height())

    def __init__(self, x_y, sprite, head=None, dialogue=False, patrol=False, speed=None):

        if not patrol:

            self.sprite = pygame.image.load(sprite)

        else:

            self.sprite_dict = {}
            self.sprite = None

            self.load_sprite(sprite)

            self.moving = False
            self.speed = speed
            x, y = x_y  # https://www.python.org/dev/peps/pep-3113/
            self.x_dir = 0
            self.y_dir = 0
            self.prev_y = 0
            self.prev_x = 0
            self.steps = self.speed * 15

            self.patrollocs = []
            self.lastpatrol = 0

        self.rect = pygame.Rect(x, y, self.sprite.get_width(), self.sprite.get_height())

        if dialogue:

            self.dialogue = True

            self.head = pygame.image.load(head)

            self.active = False

            self.dialogues = []
            self.events = []
            self.lastinit = [0, 0]
            npc.current = [0, 0]

        else:

            self.dialogue = False

    def initvars(self):
        '''reseting variables'''

        npc.currentans = 0
        npc.currentdiag = 0

    def initgui(self, screen_width, screen_height):
        '''updating the GUI'''

        self.lastinit = [npc.currentans, npc.currentdiag]
        npc.guirenderstatic = []
        npc.guirenderdynamic = []
        self.renderdyn = False  # used for making the buttons come up later than the text

        if not self.initiated:
            npc.bg.x = screen_width * 0.5 - npc.sprite_bg.get_width() / 2 + npc.sprite_headframe.get_width() / 2
            npc.bg.y = screen_height * 0.85 - npc.sprite_bg.get_height() / 2

            npc.head_x = npc.bg.left - self.head.get_width()
            npc.head_y = npc.bg.bottom - self.head.get_height()

        self.initiated = True

        npc.guirenderstatic.append([npc.sprite_bg, (npc.bg.x, npc.bg.y)])
        npc.guirenderstatic.append([npc.sprite_headframe, (npc.head_x, npc.head_y)])
        npc.guirenderstatic.append([self.head, (npc.head_x, npc.head_y)])

        npc.text_y = npc.bg.y + 3
        npc.text_x = npc.bg.x + 10

        for str in wrap_multi_line(self.dialogues[npc.currentdiag].text, npc.font, 460):
            txt = npc.font.render(str, 1, npc.textcolour)
            npc.guirenderstatic.append([txt, (npc.text_x, npc.text_y)])
            npc.text_y += txt.get_height()

        npc.answer_x = npc.bg.x + npc.sprite_bg.get_width() - npc.sprite_answer.get_width() + 13
        npc.answer_y = (npc.bg.y - npc.sprite_answer.get_height() - npc.sprite_answer.get_height() *
                        (len(self.dialogues[npc.currentdiag].answers) - 1) - npc.sprite_answer.get_height())

        for i in range(len(self.dialogues[npc.currentdiag].answers)):

            if i == npc.currentans:

                npc.guirenderdynamic.append([npc.sprite_answersel, (npc.answer_x, npc.answer_y)])

            else:

                npc.guirenderdynamic.append([npc.sprite_answer, (npc.answer_x, npc.answer_y)])

            text = npc.font.render(self.dialogues[npc.currentdiag].answers[i], 1, npc.textcolour)

            npc.text_x = npc.answer_x + npc.sprite_answer.get_width() / 2 - text.get_rect().width / 2
            npc.text_y = npc.answer_y + npc.sprite_answer.get_height() / 2 - text.get_rect().height / 2

            npc.guirenderdynamic.append([text, (npc.text_x, npc.text_y)])

            npc.answer_y += npc.sprite_answer.get_height()

    def initonlydyn(self):
        '''updating often changing parts'''

        npc.guirenderdynamic = []

        self.lastinit[0] = npc.currentans

        npc.answer_x = npc.bg.x + npc.sprite_bg.get_width() - npc.sprite_answer.get_width() + 13
        npc.answer_y = (npc.bg.y - npc.sprite_answer.get_height() - npc.sprite_answer.get_height() *
                        (len(self.dialogues[npc.currentdiag].answers) - 1) - npc.sprite_answer.get_height())

        for i in range(len(self.dialogues[npc.currentdiag].answers)):

            if i == npc.currentans:

                npc.guirenderdynamic.append([npc.sprite_answersel, (npc.answer_x, npc.answer_y)])

            else:

                npc.guirenderdynamic.append([npc.sprite_answer, (npc.answer_x, npc.answer_y)])

            text = npc.font.render(self.dialogues[npc.currentdiag].answers[i], 1, npc.textcolour)

            npc.text_x = npc.answer_x + npc.sprite_answer.get_width() / 2 - text.get_rect().width / 2
            npc.text_y = npc.answer_y + npc.sprite_answer.get_height() / 2 - text.get_rect().height / 2

            npc.guirenderdynamic.append([text, (npc.text_x, npc.text_y)])

            npc.answer_y += npc.sprite_answer.get_height()

    def display(self, screen):
        '''rendering physical'''

        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def displaygui(self, screen):
        '''rendering GUI'''

        if self.renderdyn:

            for obj in npc.guirenderdynamic:
                screen.blit(obj[0], obj[1])

        for obj in npc.guirenderstatic:
            screen.blit(obj[0], obj[1])

    def finddiag(self, name):
        '''returns a dialogue'''

        i = 0
        for diag in self.dialogues:

            if diag.name == name:
                return i

            i += 1

    def event_handler(self, event):
        '''keyboard input'''

        npc.current = [npc.currentans, npc.currentdiag]

        if self.renderdyn:  # not letting the user choose answer until the buttons are displayed

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:

                    if npc.currentans + 1 < len(self.dialogues[npc.currentdiag].answers):
                        npc.currentans += 1

                elif event.key == pygame.K_UP:

                    if npc.currentans > 0:
                        npc.currentans -= 1

                elif event.key == pygame.K_a:

                    for ev in self.events:

                        if self.dialogues[npc.currentdiag].name == ev.name:

                            if self.dialogues[npc.currentdiag].answers[
                                npc.currentans] == ev.answer or ev.answer == 'all':

                                if ev.type == 'startquest':

                                    ev.host.active = True

                                elif ev.type == 'endquest':

                                    ev.host.completed = True

                    if self.dialogues[npc.currentdiag].answers_goto[npc.currentans] == 'end':

                        self.active = False
                        npc.currentdiag = 0

                    else:

                        npc.currentdiag = self.finddiag(self.dialogues[npc.currentdiag].answers_goto[npc.currentans])

                        npc.currentans = 0

        # timer to make the answers come up after the text
        elif event.type == 24:

            self.renderdyn = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            self.active = False
            npc.currentdiag = 0
            npc.currentans = 0
            npc.guirenderstatic = []
            npc.guirenderdynamic = []

    def adddialogue(self, name, text,
                    answer1, answer1_goto,
                    answer2=None, answer2_goto=None,
                    answer3=None, answer3_goto=None,
                    answer4=None, answer4_goto=None,
                    answer5=None, answer5_goto=None, ):

        self.dialogues.append(dialogue(name, text))

        self.dialogues[-1].answers.append(answer1)
        self.dialogues[-1].answers_goto.append(answer1_goto)

        if answer2:  # using nested if statements for optimisation purposes

            self.dialogues[-1].answers.append(answer2)
            self.dialogues[-1].answers_goto.append(answer2_goto)

            if answer3:

                self.dialogues[-1].answers.append(answer3)
                self.dialogues[-1].answers_goto.append(answer3_goto)

                if answer4:

                    self.dialogues[-1].answers.append(answer4)
                    self.dialogues[-1].answers_goto.append(answer4_goto)

                    if answer5:
                        self.dialogues[-1].answers.append(answer5)
                        self.dialogues[-1].answers_goto.append(answer5_goto)

    def remdialogue(self, diag):

        # removes the dialogue, all answers pointing to it, and cleans unused dialogues

        curdialogue = self.finddiag(diag)
        referenced_dialogues = [self.dialogues[0].name]

        del self.dialogues[curdialogue]

        # checks if any of the answers reference an invalid dialogue, and deletes them if they do
        for dialog in self.dialogues:

            for goto in dialog.answers_goto:

                if goto == diag:
                    del dialog.answers[dialog.answers_goto.index(goto)]
                    dialog.answers_goto.remove(goto)

            referenced_dialogues.extend(dialog.answers_goto)

        # checks if a dialogue has no references, and deletes it if it doesnt
        for dialog in self.dialogues:

            if dialog.name not in referenced_dialogues:
                self.dialogues.remove(dialog)

    def load_sprite(self, path):
        '''loading textures'''

        up = path.split('.')[0] + '_north' + '.png'
        down = path.split('.')[0] + '_south' + '.png'
        right = path.split('.')[0] + '_east' + '.png'
        left = path.split('.')[0] + '_west' + '.png'

        files = [up, down, right, left]

        for file in files:
            ext = file.split('.')[1]
            dir = file.split('_')[1].split('.')[0]

            self.sprite_dict[dir] = pygame.image.load(file)
            self.sprite_dict[dir + '_walk'] = pygame.image.load(file.split('.')[0] + '_walking.' + ext)

        if not self.sprite:
            self.sprite = self.sprite_dict['east']

    def animate(self):
        '''updating current sprite'''

        if ((self.rect.x <= self.prev_x - self.steps) or (self.rect.x >= self.prev_x + self.steps) or
                (self.rect.y <= self.prev_y - self.steps) or (self.rect.y >= self.prev_y + self.steps)):

            if self.x_dir > 0:

                self.sprite = self.sprite_dict['east_walk']

            elif self.x_dir < 0:

                self.sprite = self.sprite_dict['west_walk']

            elif self.y_dir > 0:

                self.sprite = self.sprite_dict['south_walk']

            elif self.y_dir < 0:

                self.sprite = self.sprite_dict['north_walk']

            self.prev_x = self.rect.x
            self.prev_y = self.rect.y

        elif ((self.rect.x <= self.prev_x - self.steps / 2) or (self.rect.x >= self.prev_x + self.steps / 2) or
              (self.rect.y <= self.prev_y - self.steps / 2) or (self.rect.y >= self.prev_y + self.steps / 2)):

            if self.x_dir > 0:

                self.sprite = self.sprite_dict['east']

            elif self.x_dir < 0:

                self.sprite = self.sprite_dict['west']

            elif self.y_dir > 0:

                self.sprite = self.sprite_dict['south']

            elif self.y_dir < 0:

                self.sprite = self.sprite_dict['north']

        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.sprite.get_width(), self.sprite.get_height())

    def move(self):
        '''updates the position'''

        if self.dialogue:

            if self.active:
                self.moving = False

        if self.moving:
            self.animate()

            self.rect.x += self.x_dir * self.speed
            self.rect.y += self.y_dir * self.speed

    def addpatrol(self, locx_locy):
        locx, locy = locx_locy
        if len(self.patrollocs) <= 0:
            self.patrollocs.append([self.rect.x, self.rect.y])
        self.patrollocs.append([locx, locy])

    def updatepatrol(self, offset):

        if self.lastpatrol >= len(self.patrollocs) - 1:
            self.lastpatrol = 0

        curtar = self.patrollocs[self.lastpatrol + 1]
        curtar[0] += offset[0]
        curtar[1] += offset[1]

        curpos = (self.rect.x, self.rect.y)

        target = pygame.Rect(curtar[0], curtar[1], 0, 0)

        if inrange(self.rect, target, 25):

            self.lastpatrol += 1

        elif not inrange_x(self.rect, target, 15):

            if curtar[0] > curpos[0]:

                self.x_dir = 1
                self.y_dir = 0
                self.moving = True

            elif curtar[0] < curpos[0]:

                self.x_dir = -1
                self.y_dir = 0
                self.moving = True

        if not inrange_y(self.rect, target, 15):

            if curtar[1] > curpos[1]:

                self.x_dir = 0
                self.y_dir = 1
                self.moving = True

            elif curtar[1] < curpos[1]:

                self.x_dir = 0
                self.y_dir = -1
                self.moving = True

    def addevent(self, quest, name, answer, type):
        '''used for quests'''

        # sends a signal back to the owner when conditions are met
        e = event(quest, name, answer, type)
        self.events.append(e)
