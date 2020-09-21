from pyweek_engine import *
import pygame
import sys
import time
import random
import math
import copy
from pygame.locals import *

# important
# angles move by half a degree


class Ray:
    def __init__(self):
        self.angle = 0

        self.ray_cords = [0.0, 0.0]

        self.offset = [0.0, 0.0]

        self.distance = 0
        self.final_cords = [0.0, 0.0]

        self.color = None


class Rays:
    # until we do smt with graphics display is here as placeholder
    def __init__(self, player_angle, max_number_of_rays, display):
        max_number_of_rays += 1
        self.player_angle = player_angle
        # creating rays
        self.rays = [Ray() for _ in range(max_number_of_rays)]
        # constants
        self.degree = 0.0174533
        self.half_degree = self.degree / 2
        self.pi = math.pi
        self.half_pi = round(math.pi / 2, 6)
        self.two_pi = round(math.pi * 2, 6)
        self.three_halves_pi = round(3 * (math.pi / 2), 6)
        self.display = display
        # ray constants
        self.ray_render = 20
        self.limit = self.ray_render * 32
        self.ray_width = 5
        self.scaler = 40

    def better_distance(self, dist, angle_of_ray, angle_of_view):
        if angle_of_view > angle_of_ray:
            if angle_of_view - angle_of_ray < self.two_pi - (angle_of_view - angle_of_ray):
                return dist * math.cos(angle_of_view - angle_of_ray)
            else:
                return dist * math.cos(self.two_pi - (angle_of_view - angle_of_ray))
        else:
            if angle_of_ray - angle_of_view < self.two_pi - (angle_of_ray - angle_of_view):
                return dist * math.cos(angle_of_ray - angle_of_view)
            else:
                return dist * math.cos(self.two_pi - (angle_of_ray - angle_of_view))

    def cast_rays(self, number_of_rays, starting_ray_angle, Player_mid, game_map, player_angle):

        self.player_angle = round(starting_ray_angle, 4)
        self.rays[0].angle = self.player_angle

        for i in range(number_of_rays):

            going = 0
            to_go = 0
            aTan = round(-1 / math.tan(self.player_angle), 4)
            tan = round(math.tan(self.player_angle), 4)

            # looking up
            if self.player_angle > self.pi:
                # first ray collision
                self.rays[i].ray_cords[1] = round(((Player_mid[1] // 32) * 32) - 0.001, 3)
                self.rays[i].ray_cords[0] = round(((Player_mid[1] - self.rays[i].ray_cords[1]) * aTan) + Player_mid[0], 3)

                # offset for next collisions

                self.rays[i].offset[1] = -32
                self.rays[i].offset[0] = round(aTan * 32, 3)

            # looking down
            else:
                # first ray collision
                self.rays[i].ray_cords[1] = round(((Player_mid[1] // 32) * 32) + 32, 3)
                self.rays[i].ray_cords[0] = round(((Player_mid[1] - self.rays[i].ray_cords[1]) * aTan) + Player_mid[0], 3)

                # offset for next collisions

                self.rays[i].offset[1] = 32
                self.rays[i].offset[0] = round(-(aTan * 32), 3)

            # doing the collisions
            while going < self.ray_render:
                hit_pos = [int(self.rays[i].ray_cords[0] // 32), int(self.rays[i].ray_cords[1] // 32)]

                try:
                    if hit_pos[0] < 0 or hit_pos[1] < 0:
                        raise ValueError('A very specific bad thing happened.')

                    if game_map[hit_pos[1]][hit_pos[0]] == "1":
                        going = self.ray_render

                    else:
                        self.rays[i].ray_cords = [self.rays[i].ray_cords[0] + self.rays[i].offset[0],
                                                  self.rays[i].ray_cords[1] + self.rays[i].offset[1]]
                        going += 1

                        if going == self.ray_render:
                            self.rays[i].ray_cords[0] += 1000000
                except:
                    going = self.ray_render
                    self.rays[i].ray_cords[0] += 1000000

            # saving the dist

            first_ray_dist = distance_indicator_precise(Player_mid, copy.copy(self.rays[i].ray_cords))
            first_cords = copy.copy(self.rays[i].ray_cords)

            # looking right
            if self.player_angle > self.three_halves_pi or self.player_angle < self.half_pi:
                # first ray collision
                self.rays[i].ray_cords[0] = round(((Player_mid[0] // 32) * 32) + 32, 3)
                self.rays[i].ray_cords[1] = round(-((Player_mid[0] - self.rays[i].ray_cords[0]) * tan) + Player_mid[1], 3)

                # offset for next collisions

                self.rays[i].offset[0] = 32
                self.rays[i].offset[1] = round(tan * 32, 3)

            # looking left

            else:
                # first ray collision
                self.rays[i].ray_cords[0] = round(((Player_mid[0] // 32) * 32) - 0.001, 3)
                self.rays[i].ray_cords[1] = round(-((Player_mid[0] - self.rays[i].ray_cords[0]) * tan) + Player_mid[1], 3)

                # offset for next collisions

                self.rays[i].offset[0] = -32
                self.rays[i].offset[1] = round(-(tan * 32), 3)

            # doing the collisions

            while to_go < self.ray_render:
                hit_pos0 = [int(self.rays[i].ray_cords[0] // 32), int(self.rays[i].ray_cords[1] // 32)]

                try:

                    if hit_pos0[0] < 0 or hit_pos0[1] < 0:
                        raise ValueError('A very specific bad thing happened.')

                    if game_map[hit_pos0[1]][hit_pos0[0]] == "1":
                        to_go = self.ray_render

                    else:
                        self.rays[i].ray_cords = [self.rays[i].ray_cords[0] + self.rays[i].offset[0],
                                                  self.rays[i].ray_cords[1] + self.rays[i].offset[1]]
                        to_go += 1
                        if to_go == self.ray_render:
                            self.rays[i].ray_cords[0] += 1000000
                except:
                    to_go = self.ray_render
                    self.rays[i].ray_cords[0] += 1000000

            # saving the dist

            second_ray_dist = distance_indicator_precise(Player_mid, copy.copy(self.rays[i].ray_cords))
            second_cords = copy.copy(self.rays[i].ray_cords)

            # merging them together

            if first_ray_dist < self.limit or second_ray_dist < self.limit:
                if first_ray_dist > second_ray_dist:
                    second_ray_dist = self.better_distance(second_ray_dist, self.rays[i].angle, player_angle)
                    self.rays[i].distance = second_ray_dist
                    self.rays[i].final_cords = second_cords
                    pygame.draw.line(self.display, (0, 0, 200), [(self.ray_width * i), 225],
                                     [(self.ray_width * i) + self.ray_width, 225],
                                     int((450/second_ray_dist)*self.scaler))
                elif second_ray_dist > first_ray_dist:
                    first_ray_dist = self.better_distance(first_ray_dist, self.rays[i].angle, player_angle)
                    self.rays[i].distance = first_ray_dist
                    self.rays[i].final_cords = first_cords
                    pygame.draw.line(self.display, (0, 200, 200), [(self.ray_width * i), 225],
                                     [(self.ray_width * i) + self.ray_width, 225],
                                     int((450/first_ray_dist)*self.scaler))

            # moving angle

            self.player_angle += self.half_degree
            if self.player_angle > round(self.two_pi, 4):
                self.player_angle -= round(self.two_pi, 4)
            self.rays[i + 1].angle = round(self.player_angle, 5)

# "writing this garbage was pain" Tucan444 2020
