import arcade
import math

from asteroids.bullet import Bullet


class GlowLine(Bullet):
    def __init__(self, shadertoy, glowcolor, player, player_no):
        super().__init__(shadertoy=shadertoy, player_no=player_no)
        self.type = None
        self.shadertoy = shadertoy
        self.glowcolor = glowcolor
        self.texture = arcade.make_circle_texture(4, glowcolor)
        self._points = self.texture.hit_box_points
        self.player = player

    def draw(self):
        self.shadertoy.program['pos'] = self.position
        self.shadertoy.program['lineColor'] = arcade.get_four_float_color(self.glowcolor)
        self.shadertoy.program['angle'] = math.radians(self.angle)

        distance = arcade.math.get_distance(self.center_x, self.center_y,
                                            self.player.center_x, self.player.center_y)
        length = min(distance, 120)
        self.shadertoy.program['laserLength'] = length
        self.shadertoy.render()

    def update(self):
        """ Move the sprite """
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
