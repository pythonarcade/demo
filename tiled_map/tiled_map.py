"""
Platformer Template
"""
import arcade
from base_view import BaseView

# --- Constants
SCREEN_TITLE = "Platformer"

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class TiledMap(BaseView):
    """
    Main application class.
    """

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # A non-scrolling camera that can be used to draw GUI elements
        self.camera_gui = None

        # Keep track of the score
        self.score = 0

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False

        self.setup()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera_sprites = arcade.Camera()
        self.camera_gui = arcade.Camera()

        # Name of map file to load
        map_name = "maps/map1.json"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Keep track of the score
        self.score = 0

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # --- Other stuff
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Activate the game camera
        self.camera_sprites.use()

        # Draw our Scene
        # Note, if you a want pixelated look, add pixelated=True to the parameters
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.camera_gui.use()

        # Draw our score on the screen, scrolling it with the viewport
        self.draw_line_one("Use maps created by the Tiled Map Editor")

    def center_camera_to_player(self):
        # Find where player is, then calculate lower left corner from that
        screen_center_x = self.player_sprite.center_x - (self.camera_sprites.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera_sprites.viewport_height / 2)

        # Set some limits on how far we scroll
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Here's our center, move to it
        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)

        self.scene["Platforms"].update_animation(delta_time)
        self.scene.update(["Moving Platforms"])
        for sprite in self.scene["Moving Platforms"]:
            if sprite.right > sprite.boundary_right * TILE_SCALING and sprite.change_x > 0:
                sprite.change_x *= -1
            if sprite.left < sprite.boundary_left * TILE_SCALING and sprite.change_x < 0:
                sprite.change_x *= -1

        # self.scene["Moving Platforms"].update_animation(delta_time)
        # Move the player with the physics engine
        self.physics_engine.update()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Add one to the score
            self.score += 1

        # Position the camera
        self.center_camera_to_player()

    def on_resize(self, width, height):
        """ Resize window """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
