import random
import arcade
from base_view import BaseView

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COIN_COUNT = 500
RECT_WIDTH = 100
RECT_HEIGHT = 100


class SpatialHashDemo(BaseView):
    """ Main application class. """

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)
        self.rect = (0, RECT_WIDTH, RECT_HEIGHT, 0)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        for i in range(COIN_COUNT):
            coin = arcade.SpriteCircle(7, arcade.color_from_hex_string("#E96479"))
            coin.position = (
                random.randrange(SCREEN_WIDTH),
                random.randrange(SCREEN_HEIGHT),
            )
            self.coin_list.append(coin)
        arcade.set_background_color(arcade.color_from_hex_string("#F5E9CF"))
        self.change_x = 2
        self.change_y = 1

    def on_draw(self):
        self.clear()
        self.coin_list.draw()

        arcade.draw_lrtb_rectangle_outline(*self.rect, arcade.color_from_hex_string("#4D455D"), border_width=4)
        for y in range(0, SCREEN_HEIGHT, self.coin_list.spatial_hash.cell_size):
            for x in range(0, SCREEN_WIDTH, self.coin_list.spatial_hash.cell_size):
                arcade.draw_rectangle_outline(
                    x + self.coin_list.spatial_hash.cell_size // 2,
                    y + self.coin_list.spatial_hash.cell_size // 2,
                    self.coin_list.spatial_hash.cell_size,
                    self.coin_list.spatial_hash.cell_size,
                    color=arcade.color_from_hex_string("#4D455D"),
                )

        self.draw_line_one("Spatial Hashing for fast collision detection")

    def on_update(self, delta_time):
        """ Movement and game logic """
        """ Handle Mouse Motion """
        l, r, t, b = self.rect
        l += self.change_x
        r += self.change_x
        t += self.change_y
        b += self.change_y
        self.rect = (l, r, t, b)

        for sprite in self.coin_list:
            sprite.color = arcade.color_from_hex_string("#7DB9B6")

        l, r, t, b = self.rect
        sprites = self.coin_list.spatial_hash.get_sprites_near_rect((l, r, b, t))
        for sprite in sprites:
            sprite.color = arcade.color_from_hex_string("#E96479")

