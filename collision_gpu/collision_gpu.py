import random
from .timer import Timer
import arcade
from base_view import BaseView


SPRITE_SCALING = 1.0
COIN_COUNT = 30_000


class CollisionGPU(BaseView):

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        self.player_sprite_list = arcade.SpriteList()
        self.coin_sprite_list = arcade.SpriteList(use_spatial_hash=False)

        self.check_time = 0.0

        img = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.sprite_female = arcade.Sprite(img, 0.5)
        self.sprite_female.center_x = 180
        self.sprite_female.center_y = 100
        self.sprite_female.change_x = 2.5
        self.sprite_female.change_y = 2
        self.player_sprite_list.append(self.sprite_female)
        self.text = None
        self.timer = Timer()

        img = ":resources:images/items/coinGold.png"

        for i in range(COIN_COUNT):
            sprite = arcade.Sprite(img, 0.1)
            sprite.center_x = random.randrange(self.window.width)
            sprite.center_y = random.randrange(self.window.height)
            sprite.change_x = random.random() - 0.5
            sprite.change_y = random.random() - 0.5

            self.coin_sprite_list.append(sprite)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)
        self.total_time = 0.0

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.player_sprite_list.draw()
        self.coin_sprite_list.draw()
        self.draw_line_one("Ultra-fast collision detection")
        if self.total_time > 2.0:
            if not self.text:
                self.text = f"{COIN_COUNT:,} moving sprites using GPU: {self.timer.avg * 1000.0:.1f} ms"

            self.draw_line_two(self.text)

    def on_update(self, delta_time):
        self.sprite_female.update()
        self.coin_sprite_list.update()

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)

        with self.timer:
            collision_list = arcade.check_for_collision_with_list(self.sprite_female, self.coin_sprite_list, method=1)
        for coin in collision_list:
            coin.remove_from_sprite_lists()

