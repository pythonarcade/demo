import random
import arcade
from arcade.experimental import Shadertoy

from base_view import BaseView


class ShaderBackground(BaseView):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        self.total_time = 0.0

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.shield_list = None

        # Textures for the enemy
        self.enemy_textures = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.lives = 3
        self.death_pause = 0

        self.filter_on = True

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLACK)

        self.time = 0
        file_name = "shader_background/side_city.glsl"
        file = open(file_name)
        shader_sourcecode = file.read()
        size = self.window.width, self.window.height
        self.shadertoy = Shadertoy(size, shader_sourcecode)

        # arcade.configure_logging()

    def draw(self):
        arcade.start_render()
        self.shadertoy.render(time=self.total_time)
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
        self.total_time += delta_time
        if self.total_time > 3.0:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)
