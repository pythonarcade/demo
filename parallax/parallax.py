"""
Parallax Example
python -m arcade.examples.parallax
"""
import arcade
from base_view import BaseView

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Parallax Example"
MOVEMENT_SPEED = 5
SPRITE_SCALING = 3
BACKGROUND_SCALING = 0.5
PARALLAX_AMOUNT = 4


class ParallaxView(BaseView):
    """ Main application class. """

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        arcade.set_background_color(arcade.color.BLACK)

        self.backgrounds = arcade.SpriteList()

        self.player_sprite = arcade.SpriteSolidColor(width=20, height=30, color=arcade.color.PURPLE)
        self.player_sprite.bottom = 0
        self.player_sprite.center_x = self.window.width / 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.camera = arcade.SimpleCamera()
        self.player_sprite.change_x = -MOVEMENT_SPEED

        self.setup()

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        images = (":resources:images/hills_background/sky.png",
                  ":resources:images/hills_background/clouds.png",
                  ":resources:images/hills_background/background_hills.png",
                  ":resources:images/hills_background/middle_part.png",
                  ":resources:images/hills_background/foreground.png")
        vertical_offset = 0, 370, 40, 20, -80

        for count, image in enumerate(images):
            bottom = vertical_offset[count]

            sprite = arcade.Sprite(image, scale=BACKGROUND_SCALING)
            sprite.bottom = bottom
            sprite.left = 0
            self.backgrounds.append(sprite)

            sprite = arcade.Sprite(image, scale=BACKGROUND_SCALING)
            sprite.bottom = bottom
            sprite.left = sprite.width
            self.backgrounds.append(sprite)

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
        self.clear()

        self.camera.use()

        # Call draw() on all your sprite lists below
        self.backgrounds.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y
        self.pan_camera_to_user(0.1)

        camera_x = self.camera.position[0]

        for count, sprite in enumerate(self.backgrounds):
            layer = count // 2
            frame = count % 2
            offset = (camera_x * PARALLAX_AMOUNT) / (2 ** (layer + 1))
            jump = (camera_x - offset) // sprite.width
            final_offset = offset + (jump + frame) * sprite.width
            sprite.left = final_offset
            print(f"Count: {count} -- Offset: {final_offset}")
