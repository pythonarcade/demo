import random
from pathlib import Path

import arcade
from arcade.experimental import Shadertoy
from base_view import BaseView

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Ray-casting Demo"

SPRITE_SCALING = 0.5

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

PLAYER_MOVEMENT_SPEED = 7
BOMB_COUNT = 70
PLAYING_FIELD_WIDTH = 1600
PLAYING_FIELD_HEIGHT = 1600

RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
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
        main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"

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


class RayCasting(BaseView):

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        # The shader toy and 'channels' we'll be using
        self.shadertoy = None
        self.channel0 = None
        self.channel1 = None
        self.load_shader()

        # Sprites and sprite lists
        self.player_sprite = None
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.physics_engine = None

        self.generate_sprites()
        arcade.set_background_color(arcade.color.ARMY_GREEN)

    def load_shader(self):
        # Where is the shader file? Must be specified as a path.
        shader_file_path = Path("ray_casting/ray_casting.glsl")

        # Size of the window
        window_size = self.window.get_size()

        # Create the shader toy
        self.shadertoy = Shadertoy.create_from_file(window_size, shader_file_path)

        # Create the channels 0 and 1 frame buffers.
        # Make the buffer the size of the window, with 4 channels (RGBA)
        self.channel0 = self.shadertoy.ctx.framebuffer(
            color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
        )
        self.channel1 = self.shadertoy.ctx.framebuffer(
            color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
        )

        # Assign the frame buffers to the channels
        self.shadertoy.channel_0 = self.channel0.color_attachments[0]
        self.shadertoy.channel_1 = self.channel1.color_attachments[0]

    def generate_sprites(self):
        # -- Set up several columns of walls
        for x in range(0, PLAYING_FIELD_WIDTH, 128):
            for y in range(0, PLAYING_FIELD_HEIGHT, int(128 * SPRITE_SCALING)):
                # Randomly skip a box so the player can find a way through
                if random.randrange(2) > 0 and y != 512:
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        # -- Set some hidden bombs in the area
        for i in range(BOMB_COUNT):
            bomb = arcade.Sprite(":resources:images/tiles/bomb.png", 0.25)
            placed = False
            while not placed:
                bomb.center_x = random.randrange(PLAYING_FIELD_WIDTH)
                bomb.center_y = random.randrange(PLAYING_FIELD_HEIGHT)
                if not arcade.check_for_collision_with_list(bomb, self.wall_list):
                    placed = True
            self.bomb_list.append(bomb)

        # Create the player
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        # Physics engine, so we don't run into walls
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        # Select the channel 0 frame buffer to draw on
        self.channel0.use()
        # Draw the walls
        self.wall_list.draw()

        self.channel1.use()
        # Draw the bombs
        self.bomb_list.draw()

        # Select this window to draw on
        self.window.use()
        # Clear to background color
        self.window.clear()
        # Run the shader and render to the window
        self.shadertoy.program['lightPosition'] = self.player_sprite.position
        self.shadertoy.program['lightSize'] = 800
        self.shadertoy.render()

        # Draw the walls
        self.wall_list.draw()

        # Draw the player
        self.player_list.draw()

        self.draw_line_one("Ray-casting for shadows")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.update_animation(delta_time)
        self.player_sprite.change_x = 5
        self.player_sprite.center_x += self.player_sprite.change_x

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)


