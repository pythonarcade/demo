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
CAMERA_SPEED = 1.0

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 7

# Background color must include an alpha component
MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color(arcade.color.ALMOND)
MINIMAP_WIDTH = 600
MINIMAP_HEIGHT = 300
MAP_WIDTH = 2048
MAP_HEIGHT = 1024
MAP_MARGIN = 5


RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    texture = arcade.load_texture(filename)
    return [
        texture,
        texture.flip_vertically(),
    ]

class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = SPRITE_SCALING
        self.x_odometer = 0

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        x_change = self.center_x - self.x_odometer
        if x_change > 7:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][
                self.character_face_direction
            ]
            self.x_odometer = self.center_x


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
        self.camera_sprites = arcade.Camera()
        self.camera_gui = arcade.Camera()

        self.setup()

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = PlayerCharacter()
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
                                            path_or_texture=self.minimap_texture)

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

        self.player_sprite.update_animation(delta_time)
        self.player_sprite.change_x = 5
        self.player_sprite.center_x += self.player_sprite.change_x

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

