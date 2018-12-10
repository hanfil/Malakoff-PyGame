import pygame


# TODO:  animation functionality

class player:
    """ class for the player """

    def __init__(self, x, y, screen):

        # generic
        self.sprite = None
        self.sprite_dict = {}
        self.rect = pygame.Rect(x, y, 0, 0)
        self.disp_width = screen.get_size()[0]  # <---
        self.disp_height = screen.get_size()[1]  # <---

        # movement

        #   constants
        self.speed = 5
        self.enable_oblique = False  # flag variable to turn on or off moving in corner directions

        #   variables
        self.moving = False
        self.x_dir = 0
        self.y_dir = 0
        self.prev_y = 0
        self.prev_x = 0
        self.steps = 40

        # controls
        self.key_left = pygame.K_LEFT
        self.key_right = pygame.K_RIGHT
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN

    def display(self, screen):

        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def load_sprite(self, path):
        '''loads textures'''

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

        self.sprite = self.sprite_dict['east']
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.sprite.get_width(), self.sprite.get_height())

    def set_move(self, event):
        '''keyboard input'''

        if event.type == pygame.KEYUP:

            if event.key == self.key_left or self.key_right or self.key_down or self.key_up:

                # if a player lets go of a button while holding another one, set the move to that direction
                if pygame.key.get_pressed()[self.key_left]:

                    self.x_dir = -1
                    self.y_dir = 0

                elif pygame.key.get_pressed()[self.key_right]:

                    self.x_dir = 1
                    self.y_dir = 0

                elif pygame.key.get_pressed()[self.key_down]:

                    self.x_dir = 0
                    self.y_dir = 1

                elif pygame.key.get_pressed()[self.key_up]:

                    self.x_dir = 0
                    self.y_dir = -1

                # if the player is not holding another key stop moving
                else:
                    self.moving = False

        elif event.type == pygame.KEYDOWN:

            if event.key == self.key_left:

                self.x_dir = -1
                self.y_dir = 0
                self.moving = True

            elif event.key == self.key_right:

                self.x_dir = 1
                self.y_dir = 0
                self.moving = True

            elif event.key == self.key_down:

                self.x_dir = 0
                self.y_dir = 1
                self.moving = True

            elif event.key == self.key_up:

                self.x_dir = 0
                self.y_dir = -1
                self.moving = True

    def animate(self):
        '''updates the sprite'''

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

    def move(self, bg_map):
        '''updates the position'''

        if self.moving:

            self.animate()

            self.rect.x += self.x_dir * self.speed
            self.rect.y += self.y_dir * self.speed

            if not (self.rect.right >= 0.75 * self.disp_width
                    or self.rect.left <= 0.25 * self.disp_width
                    or self.rect.bottom >= 0.75 * self.disp_height
                    or self.rect.top <= 0.25 * self.disp_height):
                bg_map.direction = "stop"

            if self.rect.right >= 0.75 * self.disp_width:
                bg_map.direction = "right"
                self.rect.right = self.rect.right - self.speed
            elif self.rect.left <= 0.25 * self.disp_width:
                bg_map.direction = "left"
                self.rect.left = self.rect.left + self.speed
            elif self.rect.bottom >= 0.75 * self.disp_height:
                bg_map.direction = "down"
                self.rect.bottom = self.rect.bottom - self.speed
            elif self.rect.top <= 0.25 * self.disp_height:
                bg_map.direction = "up"
                self.rect.top = self.rect.top + self.speed

        else:
            bg_map.direction = "stop"

    def mapCheckMove(self, bg_map):
        if self.moving:

            if bg_map.direction == "stop" and (self.rect.right + self.speed >= 0.75 * self.disp_width
                                               or self.rect.left <= 0.25 * self.disp_width
                                               or self.rect.bottom >= 0.75 * self.disp_height
                                               or self.rect.top <= 0.25 * self.disp_height):
                print("working")
                self.rect.x += self.x_dir * self.speed
                self.rect.y += self.y_dir * self.speed

            self.animate()

        # boundary limit feature
        if self.rect.right + 1 > self.disp_width:
            self.rect.x = self.disp_width - self.rect.width + 1
        elif self.rect.x - 1 < 0:
            self.rect.x = 1

        if self.rect.bottom + 1 > self.disp_height:
            self.rect.y = self.disp_height - self.rect.height + 1
        elif self.rect.y - 1 < 0:
            self.rect.y = 1
