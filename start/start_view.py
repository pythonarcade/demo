import arcade
from base_view import BaseView
from arcade.experimental import Shadertoy


class StartView(BaseView):
    """ View to show instructions """

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        file_name = "start/neon_parallax.glsl"
        file = open(file_name)
        shader_sourcecode = file.read()
        size = self.window.width, self.window.height
        self.shadertoy = Shadertoy(size, shader_sourcecode)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.shadertoy.render(time=self.total_time)
        self.draw_line_one("The Python Arcade Library")
        if self.total_time > 2.5:
            self.draw_line_two("What can you do with it?")
        else:
            self.draw_line_two("")

    def on_update(self, delta_time):

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)
