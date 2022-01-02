"""
Work with a mini-map

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.minimap
"""

import random
from uuid import uuid4

import arcade
from pyglet.math import Vec2
from base_view import BaseView

SPRITE_SCALING = 0.5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 220

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 7

# Background color must include an alpha component
MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color(arcade.color.ALMOND)
MINIMAP_WIDTH = 600
MINIMAP_HEIGHT = 300
MAP_WIDTH = 2048
MAP_HEIGHT = 1024
MAP_MARGIN = 5


class Minimap(BaseView):
    """ Main application class. """

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        # Sprite lists
        self.player_list = None
        self.wall_list = None

        # Mini-map related

        # List of all our minimaps (there's just one)

        self.minimap_sprite_list = None

        # Texture and associated sprite to render our minimap to
        self.minimap_texture = None
        self.minimap_sprite = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None

        # Camera for sprites, and one for our GUI
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        self.setup()

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/"
                                           "femalePerson_idle.png",
                                           scale=0.4)
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        # -- Set up several columns of walls
        for x in range(0, MAP_WIDTH, 210):
            for y in range(0, MAP_HEIGHT, 64):
                # Randomly skip a box so the player can find a way through
                if random.randrange(5) > 0 and y != 512:
                    wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Construct the minimap
        size = (MINIMAP_WIDTH, MINIMAP_HEIGHT)
        self.minimap_texture = arcade.Texture.create_empty(str(uuid4()), size)
        self.minimap_sprite = arcade.Sprite(center_x=(MINIMAP_WIDTH + MAP_MARGIN) / 2,
                                            center_y=(MINIMAP_HEIGHT + MAP_MARGIN) / 2,
                                            texture=self.minimap_texture)

        self.minimap_sprite_list = arcade.SpriteList()
        self.minimap_sprite_list.append(self.minimap_sprite)

    def update_minimap(self):
        proj = 0, MAP_WIDTH, 0, MAP_HEIGHT
        with self.minimap_sprite_list.atlas.render_into(self.minimap_texture, projection=proj) as fbo:
            fbo.clear(MINIMAP_BACKGROUND_COLOR)
            self.wall_list.draw()
            self.player_sprite.draw()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        arcade.draw_rectangle_filled((MINIMAP_WIDTH + MAP_MARGIN) / 2,
                                     (MINIMAP_HEIGHT + MAP_MARGIN) / 2,
                                     MINIMAP_WIDTH + MAP_MARGIN,
                                     MINIMAP_HEIGHT + MAP_MARGIN,
                                     arcade.color.BLACK)
        # Update the minimap
        self.update_minimap()

        # Draw the minimap
        self.minimap_sprite_list.draw()
        self.draw_line_one("Create mini-maps")

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)

        self.player_sprite.center_x += 5

        # Scroll the screen to the player
        self.scroll_to_player()

    def scroll_to_player(self):
        """
        Scroll the window to the player.
        """

        # Scroll to the proper location
        position = Vec2(self.player_sprite.center_x - self.window.width / 2,
                        self.player_sprite.center_y - self.window.height / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))

