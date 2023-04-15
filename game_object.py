import math
import arcade


class Player(arcade.SpriteSolidColor):
    def __init__(self, X, Y, center_x, center_y):
        super().__init__(X, Y, arcade.color.BLUE_GRAY)
        self.X = X
        self.Y = Y
        self.center_x = center_x
        self.center_y = center_y
        self.speed = 0
    def update(self):
        self.center_x += self.speed

class Block(arcade.SpriteSolidColor):
    def __init__(self, X, Y, center_x, center_y):
        super().__init__(X, Y, arcade.color.MINT_GREEN)
        self.X = X
        self.Y = Y
        self.center_x = center_x
        self.center_y = center_y


class Ball(arcade.SpriteCircle):
    def __init__(self, speed, angle, center_x, center_y):
        super().__init__(10, arcade.color.BLUE_GRAY)
        self.angle = angle
        self.center_x = center_x
        self.center_y = center_y
        self.speed = speed
    def update(self):
        angle_rad = math.radians(self.angle)
        self.center_x += self.speed * math.cos((angle_rad))
        self.center_y += self.speed * math.sin((angle_rad))
