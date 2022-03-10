import pygame
from tile import Tile
from player import Player
from settings import tile_size, screen_width, scroll_variable


def setup_level(layout):
    player = pygame.sprite.GroupSingle()
    tiles = pygame.sprite.Group()
    for row_index, row in enumerate(layout):
        for col_index, cell in enumerate(row):
            if cell != " ":
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == "X":
                    tile = Tile((x, y), tile_size)
                    tiles.add(tile)
                if cell == "P":
                    player_sprite = Player((x, y))
                    player.add(player_sprite)

    return tiles, player


class Level:
    def __init__(self, level_data, surface):

        # setup level
        self.display_surface = surface
        self.tiles, self.player = setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < scroll_variable and direction_x < 0:
            self.world_shift = player.speed * direction_x * -1
            player.current_speed = 0
        elif player_x > screen_width - scroll_variable and direction_x > 0:
            self.world_shift = player.speed * direction_x * -1
            player.current_speed = 0
        else:
            self.world_shift = 0
            player.current_speed = player.speed

    def horizontal_movement_collisions(self):
        player = self.player.sprite
        # get player movement based on the movement of the player from keys being pressed (direction)
        player.rect.x += player.direction.x * player.current_speed
        player.collide_rect.midbottom = player.rect.midbottom

        """
        for sprite in self.tiles.sprites():
            # if player is colliding with a tile
            if sprite.rect.colliderect(player.rect):
                # if the player is moving to the right set left to the edge of the block
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                # if the player is moving to the left set right to the edge of the block
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        """
        for sprite in self.tiles.sprites():
            # if player is colliding with a tile
            if sprite.rect.colliderect(player.collide_rect):
                # if the player is moving to the right set left to the edge of the block
                if player.direction.x < 0:
                    player.collide_rect.left = sprite.rect.right
                    player.rect.midbottom = player.collide_rect.midbottom
                    player.on_left = True
                    self.current_x = player.rect.left
                # if the player is moving to the left set right to the edge of the block
                elif player.direction.x > 0:
                    player.collide_rect.right = sprite.rect.left
                    player.rect.midbottom = player.collide_rect.midbottom
                    player.on_right = True
                    self.current_x = player.rect.right
                # if x collision, set player x direction to 0
                player.direction.x = 0

        # if player is touching the left wall, and moves past the wall, or stops moving left
        if player.on_left and (player.rect.left < self.current_x or player.direction.x > 0):
            player.on_left = False
        # if player is touching the right wall, and moves past the wall, or stops moving right
        if player.on_right and (player.rect.left < self.current_x or player.direction < 0):
            player.on_right = False

    def vertical_movement_collisions(self):
        player = self.player.sprite
        # get vertical movement of the player based on the player direction (y direction from gravity and jump)
        player.apply_gravity()

        """
        for sprite in self.tiles.sprites():
            # if player is colliding with a tile
            if sprite.rect.colliderect(player.rect):
                # if the player is moving to the up, set top to the bottom edge of the block
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.on_ceiling = True
                # if the player is moving to the down, set bottom to the top edge of the block
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.on_ground = True
        """
        for sprite in self.tiles.sprites():
            # if player is colliding with a tile
            if sprite.rect.colliderect(player.collide_rect):
                # if the player is moving to the up, set top to the bottom edge of the block
                if player.direction.y < 0:
                    player.collide_rect.top = sprite.rect.bottom
                    player.rect.midbottom = player.collide_rect.midbottom
                    player.on_ceiling = True
                    player.jump_timing = 0
                # if the player is moving to the down, set bottom to the top edge of the block
                elif player.direction.y > 0:
                    player.collide_rect.bottom = sprite.rect.top
                    player.rect.midbottom = player.collide_rect.midbottom
                    player.on_ground = True

                # if y collision, set player y direction to 0
                player.direction.y = 0

        if player.on_ground and (player.direction.y < 0 or player.direction.y > 1):
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ground = False

    def run(self):
        # level camera scroll
        self.scroll_x()

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # level player
        self.player.update()
        self.horizontal_movement_collisions()
        self.vertical_movement_collisions()
        self.player.draw(self.display_surface)
        #pygame.draw.rect(self.display_surface, "red", self.player.sprite.collide_rect)
        print(self.player.sprite.stats_to_string())



