import arcade
from base_view import BaseView
import random


SPRITE_SCALING = 1.0


class MovingSprites(BaseView):

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        self.sprite_list = arcade.SpriteList()

        for i in range(10000):
            sprite = arcade.SpriteSolidColor(5, 5, arcade.color.WHITE)
            sprite.center_x = random.randrange(self.window.width)
            sprite.center_y = random.randrange(self.window.height)
            sprite.change_x = random.random() * 2 - 1
            sprite.change_y = random.random() * 2 - 1
            sprite.color = random.randrange(256), random.randrange(256), random.randrange(256)

            self.sprite_list.append(sprite)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)
        self.total_time = 0.0

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.sprite_list.draw()
        self.draw_line_one("Draw LOTS of Sprites")
        self.draw_line_two("10,000+ moving sprites")
        text = f"FPS: {arcade.get_fps(60):5.1f}"
        # print(text)

    def on_update(self, delta_time):
        self.sprite_list.update()
        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)

