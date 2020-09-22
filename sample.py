from ray_cast import *
from pyweek_engine import *

import pygame
from pygame.locals import *

import random
import sys
import math
from pathlib import Path

# !basic config
asset_path = Path('assets')
map_path = asset_path / "maps" / "map0"

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)

font = pygame.font.SysFont('Comic Sans MS', 80)
small_font = pygame.font.SysFont('Comic Sans MS', 40)
tiny_font = pygame.font.SysFont('Comic Sans MS', 20)

Window_size = [800, 600]
screen = pygame.display.set_mode(Window_size)
surface_parameters = (600, 450)
display = pygame.Surface(surface_parameters)
pygame.display.set_caption("Circle sky")
clock = pygame.time.Clock()


def sample_level(screenX):
    # !!!!!creating objects to control game

    game = Game()
    objects = Objects()
    ids = Id()

    # !!!!!creating player

    # never set direction to 0
    Player = Object("player", game.custom_id_giver, [50, 50], [0, 0], 0.01, True, [8, 8])
    Player.move.collisions = True  # enables collisions for player
    Player.move.speed = 5  # increasing speed so ur not super slow
    Player.move.offset = 30  # were creating 120 rays with 0.5 angle difference and we need player offset 30 angles
    # don't try to understand the comment above its just 30 it just is

    # simulating movement so u dont start at speed 0
    Player.dir_movement = Player.move.set_start_dir_movement(Player.direction, Player.dir_movement)

    # sorts player
    sort(Player, objects)
    # moves to next id
    game.custom_id_giver += 1

    # !!!!!creating rays

    rays = Rays(Player.direction, 120, display)

    # !!!!!creating map

    game_map = load_map("maps/map1")

    # !!!!! loading objects

    load_objects(game_map, 32, 32, objects, game)

    # !!!!! getting the dictionary for ray_casting
    # it contains textures for different blocks, numbers in map

    ray_dictionary = get_ray_dictionary()

    # !!!!!game loop

    while game.alive:
        # bg

        display.fill((0, 0, 0))
        pygame.draw.rect(display, (0, 100, 0), (0, 225, 600, 225))

        # doing player movement

        Player.movement = Player.move.move(Player.dir_movement)
        Player.direction, Player.dir_movement = Player.move.change_dir(Player.direction, Player.dir_movement,  0.05)
        # second parameter is speed of rotation

        # collisions

        objects.do_collisions(objects)

        # casting rays

        player_mid = [Player.object_pos[0] + (Player.size[0]/2), Player.object_pos[1] + (Player.size[0]/2)]
        rays.cast_rays(120, Player.direction, player_mid,
                       game_map, Player.direction + (Player.move.offset * Player.move.degree), ray_dictionary)
        # for Player_mid argument we must give middle of player
        '''
        for i in range(32):
            display.blit(pygame.transform.scale(ray_dictionary["1"].slice_textures[i], (5, 40)), (100, 100))

            screenX.blit(pygame.transform.scale(display, Window_size), (0, 0))
            pygame.display.update()
            time.sleep(0.1)
        '''

        # event loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # key_down

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pass
                    #game.alive = False

                elif event.key == K_f:
                    # remember fs = fullscreen
                    game.fs = not game.fs
                    if game.fs is False:
                        screenX = pygame.display.set_mode(Window_size)
                    else:
                        screenX = pygame.display.set_mode(Window_size, pygame.FULLSCREEN)

                elif event.key == K_d:
                    Player.move.right = True
                elif event.key == K_a:
                    Player.move.left = True
                elif event.key == K_w:
                    Player.move.forward = True
                elif event.key == K_s:
                    Player.move.backwards = True

            # key_up

            elif event.type == KEYUP:
                if event.key == K_d:
                    Player.move.right = False
                elif event.key == K_a:
                    Player.move.left = False
                elif event.key == K_w:
                    Player.move.forward = False
                elif event.key == K_s:
                    Player.move.backwards = False

        # basic loop config

        screenX.blit(pygame.transform.scale(display, Window_size), (0, 0))
        pygame.display.update()
        clock.tick(40)



def setup_map():
    """
    check file : maps/map1
    """ 

    if Path(map_path).is_file():
        pass
    else:
        import zipfile
        map_zip = asset_path / 'maps.zip'
        with zipfile.ZipFile(map_zip, 'r') as zip_ref:
            zip_ref.extractall(Path("assets"))

setup_map()
sample_level(screen)
