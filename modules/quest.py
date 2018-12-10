import pygame
from modules import playerstats

from modules.npc import *
from modules.items import *


# for a quest given by an npc
# if an item is given by item=, you also need to give the inventory with container=.

# potionquest = quest(host=self.fred, item=self.potion, container=self.inventory, needquest=knifequest,
#                 newans='Adventure',  # appends this answer to the first dialogue of the host
#                 newdiag='quest1',  # makes a new dialogue accessed by newans
#                 newtext='My mother is very sick, will you take this healing potion to her?',
#                 newans1=('Yes', 'thank'),  # the first answer is the one to end the quest
#                 newans2=('No', 'end'),
#                 npc=self.arnold, # Person to talk to
#                 gotoanswer='Potion', # answer that gets appended to the greeting dialogue
#                 diag_name='potion',
#                 diag_text='Thanks for bringing me this potion!',
#                 diag_answer1=('Bye', 'end'),
#                 change_diag='greet',
#                 change_text='Thanks for the potion!',
#                 change_ans1=('Ok', 'end'))

# for a quest given by picking up an item

# knifequest = quest(host=self.inventory, item=self.knife, # host needs to be the inventory
#                    npc=self.fred, # npc to bring the item to
#                    diag_name='greet', # diag to change, recommended to use the greetings dialogue
#                    diag_text='That\'s a shiny knife you have there, can i borrow it?',
#                    diag_answer1=('Yes', 'end'),  # the first answer is the one to end the quest
#                    diag_answer2=('No', 'end'))

# any quest with the needquest= variable will wait for that quest to complete until letting itself become active
# used for quest trees

class quest():

    def __init__(self, host=None, item=None, container=None, needquest=False,
                 newans=None,
                 newdiag=None,
                 newtext=None,
                 newans1=(None, None),
                 newans2=(None, None),
                 newans3=(None, None),
                 newans4=(None, None),
                 newans5=(None, None),
                 npc=None, gotoanswer=None,
                 diag_name=None,
                 diag_text=None,
                 diag_answer1=None,
                 diag_answer2=None,
                 diag_answer3=None,
                 diag_answer4=None,
                 diag_answer5=None,
                 change_diag=None,
                 change_text=None,
                 change_ans1=None,
                 change_ans2=None,
                 change_ans3=None,
                 change_ans4=None,
                 change_ans5=None):

        # interface bools
        self.active = False
        self.completed = False
        self.delete = False

        # state bools
        self.initialised = False
        self.activated = False
        self.donetalking = False
        self.diagremoved = False
        self.enddiagremoved = False

        self.host = host
        self.dialogue = newdiag

        if not needquest:

            self.quest = None
            self.questdone = True
            self.questtree = False

        else:

            self.quest = needquest
            self.questdone = False
            self.questtree = True

        if change_diag:
            self.change_diag = change_diag
            self.change_text = change_text
            self.change_ans1 = change_ans1
            self.change_ans2 = change_ans2
            self.change_ans3 = change_ans3
            self.change_ans4 = change_ans4
            self.change_ans5 = change_ans5

        self.newans = newans
        self.newdiag = newdiag
        self.newtext = newtext
        self.newans1 = newans1
        self.newans2 = newans2
        self.newans3 = newans3
        self.newans4 = newans4
        self.newans5 = newans5

        self.npc = npc
        self.answer = gotoanswer
        self.dialogue_name = diag_name
        self.dialogue_text = diag_text
        self.dialogue_answer1 = diag_answer1
        self.dialogue_answer2 = diag_answer2
        self.dialogue_answer3 = diag_answer3
        self.dialogue_answer4 = diag_answer4
        self.dialogue_answer5 = diag_answer5

        self.originaldiag = None

        if self.host.__module__ == "npc":

            self.type = 'npc'

            if item:

                self.item = item
                self.container = container

            else:

                self.item = False

            self.eventanswer = newans1[0]
            self.eventdiag = newdiag
            host.addevent(self, newdiag, newans1[0], 'startquest')

        elif self.host.__module__ == "container":

            self.item = item
            self.type = 'item'
            self.lastupdate = 0

    def update(self):

        if self.questtree:
            self.questdone = self.quest.delete  # .delete is a flag variable that tells the updater to remove the quest

        if self.type == 'item':

            if not self.active:

                if self.questdone:

                    self.host.items = playerstats.items

                    if len(self.host.items) > self.lastupdate:

                        self.lastupdate = len(self.host.items)
                        for item in self.host.items:

                            if item.name == self.item.name:
                                self.active = True

            else:

                if not self.activated:

                    self.originaldiag_name = self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].name
                    self.originaldiag_text = self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].text
                    self.originaldiag_answers = self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers
                    self.originaldiag_answers_goto = self.npc.dialogues[
                        self.npc.finddiag(self.dialogue_name)].answers_goto

                    self.npc.addevent(self, self.dialogue_name, self.dialogue_answer1[0], 'endquest')

                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers = []
                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers_goto = []

                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].text = self.dialogue_text
                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers.append(self.dialogue_answer1[0])
                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers_goto.append(
                        self.dialogue_answer1[1])

                    if self.dialogue_answer2:

                        self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers.append(
                            self.dialogue_answer2[0])
                        self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers_goto.append(
                            self.dialogue_answer2[1])

                        if self.dialogue_answer3:

                            self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers.append(
                                self.dialogue_answer3[0])
                            self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers_goto.append(
                                self.dialogue_answer3[1])

                            if self.dialogue_answer4:

                                self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers.append(
                                    self.dialogue_answer4[0])
                                self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers_goto.append(
                                    self.dialogue_answer4[1])

                                if self.dialogue_answer5:
                                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers.append(
                                        self.dialogue_answer5[0])
                                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers_goto.append(
                                        self.dialogue_answer5[1])

                self.activated = True

            if self.completed:

                if not self.enddiagremoved:
                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].name = self.originaldiag_name
                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].text = self.originaldiag_text
                    self.npc.dialogues[self.npc.finddiag(self.dialogue_name)].answers = self.originaldiag_answers
                    self.npc.dialogues[
                        self.npc.finddiag(self.dialogue_name)].answers_goto = self.originaldiag_answers_goto
                    playerstats.items.remove(self.item)

                self.enddiagremoved = True
                self.delete = True

        elif self.type == 'npc':

            if not self.initialised and self.questdone:
                self.host.dialogues[0].answers.insert(0, self.newans)
                self.host.dialogues[0].answers_goto.insert(0, self.newdiag)
                self.host.adddialogue(self.newdiag, self.newtext,
                                      self.newans1[0], self.newans1[1],
                                      self.newans2[0], self.newans2[1],
                                      self.newans3[0], self.newans3[1],
                                      self.newans4[0], self.newans4[1],
                                      self.newans5[0], self.newans5[1])
                self.host.addevent(self, self.eventdiag, self.eventanswer, 'startquest')  # self.active will be True
                #                                                                           when the player has
                #                                                                           used this answer

                self.initialised = True

            if self.active:

                if not self.activated:

                    if self.item:
                        self.container.add(self.item)

                    self.npc.dialogues[0].answers.insert(0, self.answer)
                    self.npc.dialogues[0].answers_goto.insert(0, self.dialogue_name)
                    self.npc.adddialogue(self.dialogue_name, self.dialogue_text, self.dialogue_answer1[0],
                                         self.dialogue_answer1[1])

                    if self.dialogue_answer2:
                        self.npc.dialogues[-1].answers.append(self.dialogue_answer2[0])
                        self.npc.dialogues[-1].answers_goto.append(self.dialogue_answer2[1])

                    if self.dialogue_answer3:
                        self.npc.dialogues[-1].answers.append(self.dialogue_answer3[0])
                        self.npc.dialogues[-1].answers_goto.append(self.dialogue_answer3[1])

                    if self.dialogue_answer4:
                        self.npc.dialogues[-1].answers.append(self.dialogue_answer4[0])
                        self.npc.dialogues[-1].answers_goto.append(self.dialogue_answer4[1])

                    if self.dialogue_answer5:
                        self.npc.dialogues[-1].answers.append(self.dialogue_answer5[0])
                        self.npc.dialogues[-1].answers_goto.append(self.dialogue_answer5[1])

                    self.npc.addevent(self, self.dialogue_name, 'all', 'endquest')

                self.activated = True

                if not self.host.active:
                    self.donetalking = True

                if not self.diagremoved and self.donetalking:
                    self.host.remdialogue(self.dialogue)
                    self.diagremoved = True

            if self.completed:

                if not self.enddiagremoved:

                    self.npc.remdialogue(self.dialogue_name)

                    if self.item:
                        self.container.rem(self.item)

                if self.change_diag:

                    self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers = []
                    self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers_goto = []
                    self.npc.dialogues[self.npc.finddiag(self.change_diag)].text = self.change_text
                    self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers.append(self.change_ans1[0])
                    self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers_goto.append(self.change_ans1[1])

                    if self.change_ans2:

                        self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers.append(self.change_ans2[0])
                        self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers_goto.append(self.change_ans2[1])

                        if self.change_ans3:

                            self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers.append(self.change_ans3[0])
                            self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers_goto.append(
                                self.change_ans3[1])

                            if self.change_ans4:

                                self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers.append(
                                    self.change_ans4[0])
                                self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers_goto.append(
                                    self.change_ans4[1])

                                if self.change_ans5:
                                    self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers.append(
                                        self.change_ans5[0])
                                    self.npc.dialogues[self.npc.finddiag(self.change_diag)].answers_goto.append(
                                        self.change_ans5[1])

                self.enddiagremoved = True
                self.delete = True
