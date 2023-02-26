import arcade
from arcade.experimental import Shadertoy

from base_view import BaseView


class ShaderBackground(BaseView):
    """ Main application class. """

    def __init__(self, time_on_screen, end_slide=False):
        super().__init__(time_on_screen)

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.shield_list = None

        self.end_slide = end_slide

        # Textures for the enemy
        self.enemy_textures = None

        arcade.set_background_color(arcade.color.BLACK)

        file_name = "shader_background/side_city.glsl"
        file = open(file_name)
        shader_sourcecode = file.read()
        size = self.window.width, self.window.height
        self.shadertoy = Shadertoy(size, shader_sourcecode)

        self.logo = arcade.load_texture("shader_background/logo-192x192.png")

        # arcade.configure_logging()

    def draw(self):
        arcade.start_render()
        self.shadertoy.render(time=self.total_time)
        if self.end_slide:
            self.draw_line_one("The Python Arcade Library")
            self.logo.draw_scaled(center_x=self.window.width * 4/5 - 35, center_y=self.window.height * 2 / 3, scale=.45)
            if self.total_time > 1.5:
                self.draw_line_two("https://arcade.academy")
            return
        self.draw_line_one("Use shaders for smooth-high performance backgrounds")

    def on_draw(self):
        """ Render the screen. """

        # Draw our stuff into the screen
        self.window.use()
        self.window.clear()
        self.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called whenever the mouse moves. """
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """
        pass

    def on_update(self, delta_time):
        if self.end_slide:
            if delta_time > 1.5:
                return

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)
