import pygame
from support import import_folder
from spritesheet import SpriteSheet
from os.path import join
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # animation
        self.frame_index = 0
        self.animation_speed = 0.15

        # player assets
        self.character_type = "Punk"
        self.animations = self.import_character_assets()
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.collide_rect = pygame.rect.Rect((0, 0), (self.rect.w, self.rect.h))

        self.collide_rect.midbottom = self.rect.midbottom

        # player movement
        self.speed = 6
        self.current_speed = self.speed
        self.direction = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0.1, 0)
        self.gravity = 0.8
        self.jump_speed = -8
        self.jump_timing = 0
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.last_status = self.status
        self.aerial_control = 0.5

    def import_character_assets(self):
        character_path = join("./assets/", self.character_type)
        animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in animations.keys():
            filename = f"{self.character_type}_{animation}.png"
            full_path = join(character_path, filename)
            #print(full_path)
            sprite_sheet = SpriteSheet(full_path)
            animations[animation] = sprite_sheet.parse_sprite_all(scale=50)
            #print(animations)

        return animations

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        #image = animation[int(self.frame_index) % len(self.animations[self.status])]
        self.frame_index += self.animation_speed

        if self.status != self.last_status:
            self.frame_index = 0
        #print(self.status, self.frame_index)
        if self.status in ['jump', 'fall']:
            if self.frame_index >= len(animation):
                self.frame_index = len(animation) - 1
        else:
            if self.frame_index >= len(animation):
                self.frame_index = 0
        image = animation[int(self.frame_index)]

        if not self.facing_right:
            # replace with flipped image
            image = pygame.transform.flip(image, True, False)

        self.image = image

        # set the rect

        """
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        elif self.on_right:
            self.rect = self.image.get_rect(midright=self.rect.midright)
        elif self.on_left:
            self.rect = self.image.get_rect(midleft=self.rect.midleft)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)
        """
        self.last_status = self.status
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        self.collide_rect.midbottom = self.rect.midbottom

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            # check if currently going the other direction and on the ground, then reset to 0 if so
            if self.direction.x < 0 and self.on_ground:
                self.direction.x = 0
            # check to make sure you are not exceeding your max speed
            if not self.direction.x > 1:
                # if on ground, acceleration is 100%
                if self.on_ground:
                    self.direction.x += self.acceleration.x
                # if not on ground, acceleration is 25%
                else:
                    self.direction.x += self.aerial_control * self.acceleration.x

            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            # check if currently going the other direction and on the ground, then reset to 0 if so
            if self.direction.x > 0 and self.on_ground:
                self.direction.x = 0

            # check to make sure you are not exceeding your max speed
            if not self.direction.x < -1:
                # if on ground, acceleration is 100%
                if self.on_ground:
                    self.direction.x += -1 * self.acceleration.x
                # if not on ground, acceleration is 25%
                else:
                    self.direction.x += -1 * self.aerial_control * self.acceleration.x
            self.facing_right = False
        else:
            if abs(self.direction.x) < 0.4:
                self.direction.x = 0
            else:
                if self.direction.x < 0:
                    self.direction.x += 0.2
                else:
                    self.direction.x += -0.2

        if keys[pygame.K_SPACE]:
            self.jump()
        elif self.jump_timing != 0:
            self.jump_timing = 0



        if keys[pygame.K_q]:
            pygame.QUIT
            exit()

    def get_status(self):
        # going up
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > self.gravity + 0.4:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                if self.on_ground:
                    self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.collide_rect.midbottom = self.rect.midbottom

    def jump(self):
        #check if player is on the ground
        if self.on_ground and self.jump_timing == 0:
            # if they are, start jumping, change to not being on the ground, and start the jump timer
            self.direction.y = self.jump_speed
            self.on_ground = False
            self.jump_timing = 1
        #reset after certain jumping timing
        elif self.jump_timing > 20:
            self.jump_timing = 0
        # check if not on ground but jump timing has started
        elif self.jump_timing > 0:
            self.direction.y += -2/self.jump_timing - 0.2
            self.jump_timing += 1
            print (self.direction.y, self.jump_timing)





    def update(self):

        self.get_input()
        self.get_status()
        self.animate()

    def stats_to_string(self):
        return [self.direction.x, self.direction.y , self.status,
                self.facing_right, self.on_ground, self.on_ceiling, self.on_left, self.on_right]




