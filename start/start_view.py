import arcade
from base_view import BaseView


class StartView(BaseView):
    """ View to show instructions """

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def on_draw(self):
        arcade.start_render()
        self.draw_line_one("What can the Arcade library do?")

    def on_update(self, delta_time):

        # High delta time probably means we just started
        if delta_time > 1.5:
            return

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)
