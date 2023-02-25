"""
Parallax Example
python -m arcade.examples.parallax
"""
import arcade
import arcade.background as background
from base_view import BaseView

# How much we'll scale up our pixel art
PIXEL_SCALE = 5

# The original & scaled heights of our background layer image data in pixels.
ORIGINAL_BG_LAYER_HEIGHT_PX = 240
SCALED_BG_LAYER_HEIGHT_PX = ORIGINAL_BG_LAYER_HEIGHT_PX * PIXEL_SCALE


PLAYER_SPEED = 300


class ParallaxView(BaseView):
    """ Main application class. """

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)
        # Set the background color to match the sky in the background images
        self.background_color = (162, 84, 162, 255)

        self.camera = arcade.SimpleCamera()
        self.text_camera = arcade.SimpleCamera()

        # Create a background group to hold all the landscape's layers
        self.backgrounds = background.ParallaxGroup()

        # Calculate the current size of each background fill layer in pixels
        bg_layer_size_px = (self.window.width, SCALED_BG_LAYER_HEIGHT_PX)

        # Import the image data for each background layer.
        # Unlike sprites, the scale argument doesn't resize the layer
        # itself. Instead, it changes the zoom level, while depth
        # controls how fast each layer scrolls. This means you have to
        # pass a correct size value when adding a layer. We calculated
        # this above.
        self.backgrounds.add_from_file(
            ":resources:/images/miami_synth_parallax/layers/back.png",
            size=bg_layer_size_px,
            depth=10.0,
            scale=PIXEL_SCALE
        )
        self.backgrounds.add_from_file(
            ":resources:/images/miami_synth_parallax/layers/buildings.png",
            size=bg_layer_size_px,
            depth=5.0,
            scale=PIXEL_SCALE
        )
        self.backgrounds.add_from_file(
            ":resources:/images/miami_synth_parallax/layers/palms.png",
            size=bg_layer_size_px,
            depth=3.0,
            scale=PIXEL_SCALE
        )
        self.backgrounds.add_from_file(
            ":resources:/images/miami_synth_parallax/layers/highway.png",
            size=bg_layer_size_px,
            depth=1.0,
            scale=PIXEL_SCALE
        )

        # Create & position the player sprite in the center of the camera's view
        self.player_sprite = arcade.Sprite(
            ":resources:/images/miami_synth_parallax/car/car-idle.png",
            center_x=self.camera.viewport_width // 2, scale=PIXEL_SCALE
        )
        self.player_sprite.bottom = 0

        # Track the player's x velocity
        self.x_velocity = PLAYER_SPEED

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)

    def on_draw(self):

        # Set up our drawing
        self.clear()
        self.camera.use()

        # Store a reference to the background layers as shorthand
        bg = self.backgrounds

        # Fake an endless world with scrolling terrain
        # Try experimenting with commenting out 1 or both of the 2 lines
        # below to get an intuitive understanding of what each does!
        bg.offset = self.camera.position  # Fake depth by moving layers
        bg.pos = self.camera.position  # Follow the car to fake infinity

        # Draw the background & the player's car
        bg.draw()
        self.player_sprite.draw(pixelated=True)

        self.text_camera.use()
        self.draw_line_one("Easy Parallax")

    def pan_camera_to_player(self):
        # Move the camera toward the center of the player's sprite
        target_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        self.camera.move_to((target_x, 0.0), 0.1)

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)

        # Move the player in our infinite world
        self.player_sprite.center_x += self.x_velocity * delta_time
        self.pan_camera_to_player()
