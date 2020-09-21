import pygame
import sys
import time
import random
import math
import copy
from pygame.locals import *

pygame.init()


def distance_indicator_precise(coords1, coords2):
    x_distance = abs(coords1[0] - coords2[0])
    y_distance = abs(coords1[1] - coords2[1])
    distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))
    return distance


def load_images(path, name, number_of_images, file_type=".png"):
    images = []
    for i in range(number_of_images):
        images.append(pygame.image.load("{}/{}_{}{}".format(path, name, i, file_type)).convert())
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
    def __init__(self, image=False):
        self.color = (255, 255, 255)

        self.pillar = []
        self.texture = image
        # waiting for slice function from bung
        self.slice_texture = []


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
            if obj == "1":
                obj = Object("solid", game.custom_id_giver, [x, y], [0, 0], 0, False, [width, height])
                sort(obj, objects)
                game.custom_id_giver += 1
            x += width
        y += height
        x = 0
