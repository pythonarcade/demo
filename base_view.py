import arcade


class BaseView(arcade.View):
    def draw_line_one(self, text, color=arcade.color.BLACK):
        arcade.draw_text(text, self.window.width / 2, self.window.height * 2 / 3,
                         color, font_size=50, anchor_x="center")