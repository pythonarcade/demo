import math
import arcade
from asteroids.bullet import Bullet


class GlowImageSprite(Bullet):
    """ Sprite that sets its angle to the direction it is traveling in. """
    def __init__(self, name, scale, shadertoy, glowcolor, player_no):
        super().__init__(name, scale, shadertoy, player_no=player_no)
        self.type = None
        self.shadertoy = shadertoy
        self.glowcolor = glowcolor

    def draw(self):
        self.shadertoy.program['pos'] = self.position
        self.shadertoy.program['color'] = arcade.get_three_float_color(self.glowcolor)
        self.shadertoy.render()

    def update(self):
        """ Move the sprite """
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
