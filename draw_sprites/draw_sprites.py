import arcade
from base_view import BaseView


SPRITE_SCALING = 1.0


class DrawSprites(BaseView):

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        self.sprite_list = arcade.SpriteList()

        img = ":resources:images/tiles/grassMid.png"

        for i in range(31):
            sprite = arcade.Sprite(img, 0.5)
            sprite.center_x = i * sprite.width
            sprite.center_y = 450
            self.sprite_list.append(sprite)

        img = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.sprite_female = arcade.Sprite(img, 1)
        self.sprite_female.center_x = 800
        self.sprite_female.center_y = 546
        self.sprite_list.append(self.sprite_female)

        img = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.sprite_female = arcade.Sprite(img, 1)
        self.sprite_female.center_x = 950
        self.sprite_female.center_y = 546
        self.sprite_list.append(self.sprite_female)

        img = ":resources:images/tiles/grass_sprout.png"
        self.sprite_female = arcade.Sprite(img, 1)
        self.sprite_female.center_x = 900
        self.sprite_female.center_y = 546
        self.sprite_list.append(self.sprite_female)

        self.camera = arcade.SimpleCamera()
        # arcade.load_font("fonts/TELONE-Regpersonal.otf")

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)
        self.total_time = 0.0

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.camera.use()
        self.sprite_list.draw()
        self.draw_line_one("Draw Sprites")

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)

