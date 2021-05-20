import pygame, sys, json
from config import *


class Transformation:
    @classmethod
    def resize(cls, sprite_obj) -> object:
        """
        Resize sprite based in screen resolution / sprite resolution
        """

        transform_size = [
            int(SCREENWIDTH / 2),
            int(SCREENHEIGHT / 2)
        ]
        spr_transform = pygame.transform.scale(
            sprite_obj[0], (sprite_obj[1][0] * 4, sprite_obj[1][1] * 4))
        return spr_transform


class Spritesheet:
    def __init__(self, filename):
        """
        Prepare json spritesheet parsing
        """

        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.meta_data = self.filename.replace('png', 'json')

        """
        Try/Except for handling sprite not found
        """

        try:
            with open(self.meta_data) as f:
                self.data = json.load(f)
            f.close()
        except Exception as err:
            print(f"{err}")
            sys.exit()

    def fix_spr(self, spr_obj):
        """
        Sprite fixes, such as color and transparency issues
        """
        spr_obj[0] = Transformation.resize(spr_obj)
        spr_obj[0] = spr_obj[0].convert_alpha()
        return spr_obj

    def get_spr(self, xCord: int, yCord: int, width: int, height: int) -> list:
        """
        Get sprite from json based in coordinates (X, Y, W, H)
        """

        self.sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        self.sprite.blit(self.sprite_sheet, (0, 0),
                         (xCord, yCord, width, height))

        self.spr_rect = self.sprite.get_rect()
        self.size = self.sprite.get_size()

        self.sprite_handled = self.fix_spr(
            [self.sprite, self.size, self.spr_rect])
        return self.sprite_handled

    def parse_spr(self, name: str) -> object:
        """
        Parse json sprite name to json sprite coord and pass to get_spr
        Recomended to call this insted of get_spr, since its a wrapper around get_spr
        """

        sprite = self.data['frames'][name]['frame']
        xCord, yCord, width, height = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_spr(xCord, yCord, width, height)
        return image