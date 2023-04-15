import math
import random

import arcade
from game_object import Player
from game_object import Ball
from game_object import Block


import pymunk

# definicion de constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1200
SCREEN_TITLE = "Briccs"

SPEED = 7
BALLSPEED = 9

def mirrorerY(angle):  
    if 180 >= angle > 0:
     mirrored_angle = 180 - angle
    else:
     mirrored_angle = 360 - (angle -  180)   
    return mirrored_angle

def mirrorerX(angle):
    if 180 >= angle > 0:
        mirrored_angle = 360 - angle
    else:
        mirrored_angle = 180 - (angle - 180)
    return mirrored_angle

class App(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.sprites = arcade.SpriteList()
        self.player = Player(150, 20, 400, 200)
        self.sprites.append(self.player)
        self.ball = Ball(BALLSPEED, 271, 400, 350)
        self.sprites.append(self.ball)
        self.blocks = arcade.SpriteList()
        self.score = 0
        self.over = 0;
        for x in [50, 150, 250, 350, 450, 550, 650, 750]:
            for y in [1175, 1125, 1075, 1025, 975, 925, 875, 825]:
                block = Block(
                    90, 46,
                    x, y
                )
                self.blocks.append(block)
                self.sprites.append(block)


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.player.speed = -SPEED
            print('Pressed Left.')
        if symbol == arcade.key.RIGHT:
            self.player.speed = SPEED
            print('Pressed Right.')

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.speed = 0

    def on_update(self, delta_time: float):
        """Metodo para actualizar objetos de la app"""
        if(self.over == 0):
            if self.player.center_x-75 >= 0 and self.player.center_x+75 <= SCREEN_WIDTH: 
             self.player.update()
            if self.player.speed > 0 and self.player.center_x-75 <= 0:
             self.player.update()  
            if self.player.speed < 0 and self.player.center_x+75 >= SCREEN_WIDTH:
             self.player.update()    
            self.ball.update()
            self.blocks_update()
            self.ball_update()
        else:
            for s in self.sprites:
              self.sprites.remove(s)
            self.player = 0;
            self.ball = 0;

    def on_draw(self):
        """Metodo para dibujar en la pantalla"""
        if(self.over == 0):
            arcade.start_render()
            self.sprites.draw()
            arcade.draw_text(
                f"Score: {self.score}",
                600,
                35,
                arcade.color.YELLOW,
                20,
                width=SCREEN_WIDTH,
                align="left"
            )
        else:
            self.clear()
            arcade.draw_text('GAME OVER !', 200, 600, arcade.color.WHITE, 54);       
            arcade.draw_text(
                f"Score: {self.score}",
                600,
                35,
                arcade.color.YELLOW,
                20,
                width=SCREEN_WIDTH,
                align="left"
            )

    def blocks_update(self):
        return
    
    def playerdistangle(self):
        return


    def ball_update(self):
        if arcade.check_for_collision(self.ball, self.player):
            print('hit player top')
            #self.ball.angle = mirrorerX(float(self.ball.angle));
            dd = ((abs(self.ball.center_x-self.player.center_x)/self.player.center_x))
            #print(dd)
            if(self.ball.center_x-self.player.center_x>0):
             self.ball.angle = mirrorerX(float(self.ball.angle))-dd*200
            else:
             self.ball.angle = mirrorerX(float(self.ball.angle))+dd*200

        if (self.ball.center_y+10) > SCREEN_HEIGHT:
            #print(self.ball.angle)
            self.ball.angle = mirrorerX(float(self.ball.angle));
            #print('hit screen top')
  
        if (self.ball.center_x+10) > SCREEN_WIDTH-1:
            #print(self.ball.angle)
            self.ball.angle = mirrorerY(self.ball.angle)
            #print('hit screen right side')
        if (self.ball.center_x-10) < 1:
            #print(self.ball.angle)
            self.ball.angle = mirrorerY(self.ball.angle)
            #print('hit screen left side')

        for b in self.blocks:
            #Encontre el error, si se checkea la distancia entre el borde
            # derecho o izquierdo de la bola y del bloque, el orden de la
            #veriicacion a veces hace verdad que detecte la cercania de Y
            #o de X cuando no deberia, y el angulo lo cambia mal.
            if arcade.check_for_collision(self.ball, b):
             print('collision with block!')
             #self.blocks.update_color(b)
             b.remove_from_sprite_lists()
             self.score += 1;
            #idea, calcular donde colisiono usando el angluo de la distancia
            #entre centro de bola y centro de bloque.
             angleR1 = math.degrees(math.atan(23/55))
             angleR2 = mirrorerX(angleR1)
             angleL1 = mirrorerY(angleR1)
             angleL2 = 180+angleR1
             ydif = self.ball.center_y - b.center_y
             xdif = self.ball.center_x - b.center_x
             dist = math.sqrt(abs(xdif)+abs(ydif))
             if ydif > 0:
                if xdif >= 0:
                    if math.degrees(math.atan(abs(ydif/xdif))) >= angleR1:
                        print('collision with topright of block')
                        self.ball.angle = mirrorerX(self.ball.angle)
                    else:
                        print('collision with upperright of block')
                        self.ball.angle = mirrorerY(self.ball.angle)
                else:
                    if math.degrees(math.atan(abs(ydif/xdif))) >= angleR1:
                        print('collision with topleft of block')
                        self.ball.angle = mirrorerX(self.ball.angle)
                    else:
                        print('collision with upperleft of block')
                        self.ball.angle = mirrorerY(self.ball.angle)
             else:
                if xdif >= 0:    
                    if math.degrees(math.atan(abs(ydif/xdif))) >= angleR1:
                        print('collision with bottomright of block')
                        self.ball.angle = mirrorerX(self.ball.angle)
                    else:
                        print('collision with lowerright of block')
                        self.ball.angle = mirrorerY(self.ball.angle)
                else:
                    if math.degrees(math.atan(abs(ydif/xdif))) >= angleR1:
                        print('collision with bottomleft of block')
                        self.ball.angle = mirrorerX(self.ball.angle)
                    else:
                        print('collision with lowerleft of block')
                        self.ball.angle = mirrorerY(self.ball.angle) 
        if (self.ball.center_y-10) <= 0:
            print('hit screen bottom')  
            self.over = 1;     

if __name__ == "__main__":
    app = App()
    arcade.run()
