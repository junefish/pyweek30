import pygame
import sys
import time
import random
import math
import copy
from pygame.locals import *

pygame.init()


# has attributes for basic thing in game
class Game:
    def __init__(self, game_maps=None):
        self.alive = True
        # fs = fullscreen
        self.fs = False
        self.custom_id_giver = 0

        self.game_maps = None
        # checks if there are any maps if there are puts them in self.game_maps
        if game_maps is not None:
            self.game_maps = game_maps


# stores objects in a sorted way
class Objects:
    def __init__(self):
        self.game_objects = []
        self.collision_objects = []
        self.moving_objects = []

        # dunno if next att will be useful
        # u add ids of objects u want to delete there is no func to delete for now

        self.objects_to_delete = []

    def do_collisions(self, objects):
        for obj in self.collision_objects:
            collision(obj, objects)

    def destroy_trash(self, ids):
        for trash in self.objects_to_delete:
            ids.removed_id.append(trash)
        self.objects_to_delete = []


# Id class just stores all ids of all objects
class Id:
    all_ids = []
    ids_to_remove = []


# collisions class take care of collision funcs
# !!!!!!!!!! holds init for Object !!!!!!!!!!!!!!!!!!!
# class purely for inheritance
class Collisions(Id):

    def __init__(self, typeX, object_id, x_y, movement, direction, moving, size):
        self.type = typeX
        self.object_id = object_id
        self.object_pos = x_y
        self.movement = movement
        self.direction = direction
        self.moving = moving
        self.size = size
        self.dir_movement = [0.0, 0.0]
        self.memory = []
        if self.object_id != self.all_ids:
            self.all_ids.append(self.object_id)
        else:
            print("duplicate/ linked object")

        # giving it bonus classes

        if self.moving:
            self.move = Moving_Object()

        self.rect = pygame.Rect(self.object_pos[0], self.object_pos[1], self.size[0], self.size[1])

    # theres a function for every type of collisions
    # edit collisions here (I added some basic ones just so u can see)
    # self if objects that it hit and obj is the object that hit smt

    # always add both side of collisions (ask who collided with whom)

    def hit_bottom(self, obj, objects):
        if self.type == "solid":
            if obj.type == "player":
                obj.rect.bottom = self.rect.top
                obj.object_pos = [obj.rect.x, obj.rect.y]

    def hit_top(self, obj, objects):
        if self.type == "solid":
            if obj.type == "player":
                obj.rect.top = self.rect.bottom
                obj.object_pos = [obj.rect.x, obj.rect.y]

    def hit_left(self, obj, objects):
        if self.type == "solid":
            if obj.type == "player":
                obj.rect.left = self.rect.right
                obj.object_pos = [obj.rect.x, obj.rect.y]

    def hit_right(self, obj, objects):
        if self.type == "solid":
            if obj.type == "player":
                obj.rect.right = self.rect.left
                obj.object_pos = [obj.rect.x, obj.rect.y]


# used to create templates for ray caster
class Ray_cast_block:
    def __init__(self, image=None, color_key=(0, 0, 0)):
        self.color = (255, 255, 255)
        self.color_key = color_key

        self.pillar = []
        self.texture = image
        self.image = False
        self.slice_textures = []

        if image is not None:
            self.texture.set_colorkey(color_key)
            self.image = True
            self.slice_it_up()

    def slice_it_up(self):
        image_slice = self.get_slice_rectangles()
        for sliceX in image_slice:
            image1 = pygame.Surface((1, 32)).convert()
            image1.blit(self.texture, sliceX)
            image1.set_colorkey(self.color_key)
            self.slice_textures.append(image1)

    @staticmethod
    def get_slice_rectangles():
        image_slices = []
        x = -32
        y = 0
        while y <= 32:
            sliceX = pygame.Rect(x, 0, 32, 32)  # loads one slice of the image at a time.
            image_slices.append(0)
            image_slices[y] = sliceX
            x += 1
            y += 1
        del image_slices[0]
        return image_slices  # [:-1]


# next 2 classes are for object class
class Moving_Object:
    def __init__(self):
        # consts
        self.degree = 0.0174533
        self.pi = math.pi
        self.half_pi = round(math.pi / 2, 6)
        self.two_pi = round(math.pi * 2, 6)
        self.three_halves_pi = round(3 * (math.pi / 2), 6)

        self.speed = 1
        self.offset = 0

        self.forward = False
        self.backwards = False
        self.left = False
        self.right = False

        self.collisions = False

    def move(self, dir_movement):
        movement = [0.0, 0.0]

        if self.forward:
            movement = dir_movement
        if self.backwards:
            movement = [-dir_movement[0], -dir_movement[1]]

        return movement

    # dir is the angle the player is facing
    def change_dir(self, direction, dir_movement, angle):
        if self.left:
            direction -= angle
            if direction < 0:
                direction += self.two_pi
            dir_movement[0] = round(math.cos(direction + (self.offset * self.degree)) * self.speed, 2)
            dir_movement[1] = round(math.sin(direction + (self.offset * self.degree)) * self.speed, 2)
        if self.right:
            direction += angle
            if direction > self.two_pi:
                direction -= self.two_pi
            dir_movement[0] = round(math.cos(direction + (self.offset * self.degree)) * self.speed, 2)
            dir_movement[1] = round(math.sin(direction + (self.offset * self.degree)) * self.speed, 2)

        return direction, dir_movement

    # used for setting things before game loop
    def set_start_dir_movement(self, direction, dir_movement):
        dir_movement[0] = round(math.cos(direction + (self.offset * self.degree)) * self.speed, 2)
        dir_movement[1] = round(math.sin(direction + (self.offset * self.degree)) * self.speed, 2)
        return dir_movement


class Object(Collisions):
    def __init__(self, typeX, object_id, x_y, movement, direction, moving, size):
        super().__init__(typeX, object_id, x_y, movement, direction, moving, size)

    def __str__(self):
        return self.type

    # changes position along with the rect
    def change_pos(self, x_y):
        self.object_pos = x_y
        self.rect = pygame.Rect(self.object_pos[0], self.object_pos[1], self.size[0], self.size[1])


# yes i still havent learned threading so thats that
class Timers:
    def __init__(self):
        self.timers = []

        # stuff under this is for separate functions

        self.wall_images = load_images("assets/textures/animation1", "wall", 5)

    @staticmethod
    def ray_timer_advance(timer, ray_dict):
        timer.image_number += 1

        ray_dict[timer.extras[0]] = Ray_cast_block(timer.extras[1][timer.image_number % len(timer.extras[1])])

    # with type of timer u decide what to use
    def add_timer(self, duration, repeat, type_of_timer):

        if type_of_timer == "ray_wall_animation":
            self.timers.append([Timer(duration, repeat, ["5", self.wall_images], type_of_timer),
                                self.ray_timer_advance])

    # parameters passed into are for the funcs
    def add_time(self, ray_dict):
        for timer in self.timers:
            timer[0].step += 1

            if timer[0].step == timer[0].duration:
                if timer[0].type == "ray_wall_animation":
                    timer[1](timer[0], ray_dict)

                    if timer[0].repeat:
                        timer[0].step = 0
                    else:
                        self.timers.remove(self.timers.index(timer))


class Timer:
    def __init__(self, duration, repeat, extras, type_of_timer):
        self.duration = duration
        self.repeat = repeat
        self.step = 0
        self.extras = extras
        self.type = type_of_timer

        # bonus att

        self.image_number = 0


def distance_indicator_precise(coords1, coords2):
    x_distance = abs(coords1[0] - coords2[0])
    y_distance = abs(coords1[1] - coords2[1])
    distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))
    return distance


def load_images(path, name, number_of_images, file_type=".png"):
    images = []
    for i in range(number_of_images):
        images.append(pygame.image.load("{}/{}{}{}".format(path, name, i, file_type)).convert())
    return images


def load_map(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    product = []
    for line in data:
        product.append(list(line))
    return product


# next func sorts object into objects class so the objects is stored where it should be
def sort(obj, objects):
    objects.game_objects.append(obj)

    if obj.moving:
        objects.moving_objects.append(obj)

        if obj.move.collisions:
            objects.collision_objects.append(obj)


def find_collisions(obj, objects):
    hit_list = []
    for element in objects.game_objects:
        if element.object_id != obj.object_id:
            if element.rect.colliderect(obj.rect):
                hit_list.append(element)
    return hit_list


def collision(obj, objects):
    # collisions for left/right
    obj.change_pos([obj.object_pos[0] + obj.movement[0], obj.object_pos[1]])
    hit_list = find_collisions(obj, objects)
    for item in hit_list:
        if obj.movement[0] > 0:
            item.hit_right(obj, objects)
        elif obj.movement[0] < 0:
            item.hit_left(obj, objects)

    # collisions for top/bottom
    obj.change_pos([obj.object_pos[0], obj.object_pos[1] + obj.movement[1]])
    hit_list = find_collisions(obj, objects)
    for item in hit_list:
        if obj.movement[1] > 0:
            item.hit_bottom(obj, objects)
        elif obj.movement[1] < 0:
            item.hit_top(obj, objects)


# !!!!!!!!!!! config this function for every program !!!!!!!!!!
def load_objects(game_map, width, height, objects, game):
    x, y = 0, 0
    for line in game_map:
        for obj in line:
            # this is just to be efficient normaly u can use elif and put another obj to another num
            if obj in ["1", "2", "3", "4", "5"]:
                obj = Object("solid", game.custom_id_giver, [x, y], [0, 0], 0, False, [width, height])
                sort(obj, objects)
                game.custom_id_giver += 1
            x += width
        y += height
        x = 0


# !!!!!!!!!! config this function makes template for ray casting !!!!!!!!!!!!!!
def get_ray_dictionary():
    # u can also just define a color, usually u do a texture, pillars are not usable yet(if they'll ever be)
    blocks = {
        "0": Ray_cast_block(),
        "1": Ray_cast_block(pygame.image.load("assets/textures/test_texture.png")),
        "2": Ray_cast_block(pygame.image.load("assets/textures/test_texture0.png")),
        "3": Ray_cast_block(),
        "4": Ray_cast_block(pygame.image.load("assets/textures/test_transparent.png")),
        "5": Ray_cast_block(pygame.image.load("assets/textures/animation1/wall0.png"))
    }
    blocks["3"].color = (200, 30, 10)
    return blocks
