import arcade


SPRITE_SCALING = 1.0


class DrawSprites(arcade.View):

    def __init__(self):
        super().__init__()
        self.total_time = 0.0

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

        # arcade.load_font("fonts/TELONE-Regpersonal.otf")

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.sprite_list.draw()
        arcade.draw_text("Draw Sprites", self.window.width / 2, self.window.height * 2 / 3,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.total_time > 2.0:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)

