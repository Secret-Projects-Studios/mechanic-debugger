#!/usr/bin/python3

import sys
import random
import json
import asyncio
import os
import inspect
import contextlib
import signal
import math
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *
from itertools import cycle
from typing import TypeVar
import threading
from threading import Thread, Lock
from multiprocessing import Process
import logging
from graphical import Transformation, Spritesheet
from config import *


"""
Entity definitions
"""

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        sprites.add(self, layer=0)
        parsed_spr = Spritesheet('./assets/sprites.png')
        self.PLAYER_SPR = [
            parsed_spr.parse_spr("0.png"),
            parsed_spr.parse_spr("2.png"),
            parsed_spr.parse_spr("1.png")
        ]
        self.index = 0
        self.image = self.PLAYER_SPR[self.index][0]
        self.frame_delay = 75
        self.rect = self.PLAYER_SPR[self.index][0].get_rect(center=position)

    def update(self):
        global last_update, FACING_DIRECTION, moved
        self.flipped_image = pygame.transform.flip(
                        self.PLAYER_SPR[self.index][0], True, False)

        current_time = pygame.time.get_ticks()

        print(moved)
        if moved == True:
            moved = False
            if current_time - last_update >= self.frame_delay:
                if FACING_DIRECTION == "right":
                    self.image = self.PLAYER_SPR[self.index][0]
                else:
                    self.image = self.flipped_image
                self.index += 1
                if self.index == 3:
                    self.index = 0
                last_update = current_time
        else:
            if FACING_DIRECTION == "right":
                self.image = self.PLAYER_SPR[2][0]
            if FACING_DIRECTION == "left":
                self.image = pygame.transform.flip(
                        self.PLAYER_SPR[2][0], True, False)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        sprites.add(self, layer=0)

        parsed_spr = Spritesheet('./assets/blocks.png')
        self.OBJ_SPR = [
            parsed_spr.parse_spr("0.png"),
            parsed_spr.parse_spr("2.png"),
            parsed_spr.parse_spr("1.png")
        ]
        self.image = self.OBJ_SPR[0][0]
        self.rect = self.OBJ_SPR[0][0].get_rect(center=position)



class Behavior:
    def __init__(self):
        print("Behavior Initialized")

    def offline(self, left, right, control, player):
        global FACING_DIRECTION, moved
        self.left = left
        self.right = right
        self.control = control
        if self.left == True:
            if self.control == True:
                player.rect.x -= 5
            else:
                player.rect.x -= 5
            FACING_DIRECTION = "left"
            self.left = False
            self.right = False

        if self.right == True:
            if self.control == True:
                player.rect.x += 5
            else:
                player.rect.x += 5
            FACING_DIRECTION = "right"
            self.right = False
            self.left = False
        sprites.update()

    def online(self):
        return 0


class Controller():
    """
    Parse user input keys from pygame to graphical actions
    """

    def __init__(self):
        pygame.key.set_repeat(50, 20)
        self.delay = 100
        self.neutral = True
        self.pressed = 0
        self.left = False
        self.right = False
        self.isJumping = False
        self.control = False
        self.count = 0
        self.crouch = False
        self.connection_behavior = Behavior()

        print("Controller Initialized")

    def parse_control(self,  player, control, event):
        global last_update, moved, GAME_METHOD
        self.isJumping = False

        # log_data("debug", event, self.__class__.__name__, inspect.stack()[0][3])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
                moved = True

            if event.key == pygame.K_RIGHT:
                self.right = True
                moved = True

            if event.key == (pygame.K_SPACE or pygame.K_UP):
                self.isJumping = True
                moved = True

            if event.key == pygame.K_DOWN:
                self.crouch = True
                moved = True

            if event.key == pygame.K_ESCAPE:
                Configuration.exit()

        if control or event.type == JOYDEVICEADDED and event.type is not (pygame.KEYDOWN or pygame.KEYUP):

            if event.type == JOYBUTTONUP:
                self.control = True
                print(event)

            if event.type == JOYDEVICEREMOVED:
                self.control = False
                control = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                print("Controller removed")

            if event.type == JOYDEVICEADDED:
                self.control = True
                control = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                print("Controller added")

            if math.ceil(control[0].get_axis(0)) == 0:
                self.control = False
                self.neutral = True

            if event.type == JOYAXISMOTION:
                if math.ceil(control[0].get_axis(0)) == -1:
                    self.control = True
                    self.left = True
                    moved = True
                    self.neutral = False

            if math.ceil(control[0].get_axis(0)) == 1:
                self.control = True
                self.right = True
                moved = True
                self.neutral = False

        log_data("debug", f"Right :: {self.right} | Left :: {self.left}", self.__class__.__name__, inspect.stack()[0][3])

        if GAME_METHOD == True:
            self.connection_behavior.offline(self.left, self.right, self.control, player)
        else:
            self.connection_behavior.offline(self.left, self.right, self.control, player)
        self.control = False
        self.right = False
        self.left = False


class World:
    def __init__(self):
        print("World Initialized")


class Configuration:
    def __init__(self):
        print("Configuration Initialized")

    @classmethod
    def exit(self):
        os.kill(os.getpid(), signal.SIGINT)

    @classmethod
    def update_fps(self, font):
        fps = str(f"FPS :: {int(FPSCLOCK.get_fps())}")
        fps_text = font.render(fps, 1, pygame.Color("black"))
        return fps_text



def main():
    """
    game mainloop
    """
    try:
        """
        Construction player sprite pattern
        """

        pygame.init()
        pygame.display.set_caption(r"School Panic!")
        controller = Controller()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(
            i) for i in range(pygame.joystick.get_count())]
        Player.groups = sprites, players
        Obstacle.groups = sprites, obstacles
        player = Player((PLAYERX, BASEY))
        obs = Obstacle((150, BASEY))
        font = pygame.font.SysFont("Arial", 18)
        while True:
            SCREEN.fill((198, 39, 62))
            SCREEN.blit(Configuration.update_fps(font), (10, 0))
            for event in pygame.event.get():
                controller.parse_control(player, joysticks, event)
            sprites.draw(SCREEN)
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    except KeyboardInterrupt:
        """
        Handling keyboard interruption (usually Ctrl+C) to exit the program.
        beautifully
        """
        Configuration.exit()
    except Exception as error:
        logging.exception("Exception occurred :: {error}")


if __name__ == "__main__":
    """
    Debug preferences
    """
    main()
