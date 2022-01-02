import arcade


class BaseView(arcade.View):
    def __init__(self, time_on_screen):
        super().__init__()
        self.total_time = 0.0
        self.time_on_screen = time_on_screen

    def draw_line_one(self, text, color=arcade.color.BLACK):
        arcade.draw_rectangle_filled(self.window.width / 2, self.window.height * 2 / 3 + 20, self.window.width, 100,
                                     color=arcade.color.ALMOND)
        arcade.draw_text(text, self.window.width / 2, self.window.height * 2 / 3,
                         color, font_size=55, anchor_x="center", font_name="Cabin Sketch")
