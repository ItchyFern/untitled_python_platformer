import pygame
import json


class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        print(self.meta_data)
        with open(self.meta_data) as f:
            self.data = json.load(f)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['Frames'][name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        return self.get_sprite(x, y, w, h)

    def parse_sprite_all(self, scale=None):
        sprite_list = []
        for key in self.data["Frames"]:
            sprite = self.parse_sprite(key)
            if scale is not None:
                x = sprite.get_rect().w
                y = sprite.get_rect().h
                scale_decimal = scale/y
                #print(scale_decimal, scale_decimal*x, scale_decimal*y)
                sprite = pygame.transform.scale(sprite, (int(x * scale_decimal), int(y*scale_decimal)))
            sprite_list.append(sprite)
        return sprite_list
