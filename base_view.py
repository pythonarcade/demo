import arcade


class BaseView(arcade.View):
    def __init__(self, time_on_screen):
        super().__init__()
        self.total_time = 0.0
        self.time_on_screen = time_on_screen

    def draw_line_one(self, text, color=arcade.color.BLACK):
        x = self.window.width / 2
        y_box = self.window.height * 2 / 3
        y_text = y_box - 20
        arcade.draw_rectangle_filled(x, y_box, self.window.width, 100,
                                     color=arcade.color.ALMOND)
        arcade.draw_text(text, self.window.width / 2, y_text,
                         color, font_size=55, anchor_x="center", font_name="Cabin Sketch")

    def draw_line_two(self, text, color=arcade.color.BLACK):
        x = self.window.width / 2
        y_box = self.window.height * 2 / 3 - 80
        y_text = y_box - 20
        arcade.draw_rectangle_filled(x, y_box, self.window.width, 80,
                                     color=arcade.color.ALMOND)
        arcade.draw_text(text, self.window.width / 2, y_text,
                         color, font_size=55, anchor_x="center", font_name="Cabin Sketch")
