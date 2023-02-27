import arcade
from base_view import BaseView
from arcade.experimental import Shadertoy


LINE_HEIGHT = 90


class FeatureListView(BaseView):
    """ View to show instructions """

    def __init__(self, time_on_screen, item_list):
        super().__init__(time_on_screen)
        self.item_list = item_list
        self.time_per_item = time_on_screen / (len(self.item_list))

    def on_show(self):
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        color = arcade.color.BLACK
        y_text = self.window.height / 2
        y_text += (LINE_HEIGHT * len(self.item_list)) / 2
        for count, text in enumerate(self.item_list):
            if count * self.time_per_item < self.total_time:
                arcade.draw_text(text, self.window.width / 2, y_text,
                                 color, font_size=55, anchor_x="center", font_name="Cabin Sketch")
            y_text -= LINE_HEIGHT

    def on_update(self, delta_time):

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)
