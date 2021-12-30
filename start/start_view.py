import arcade


class StartView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        super().__init__()
        self.total_time = 0.0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("What can the Arcade library do?", self.window.width / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.total_time > 2.0:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)
