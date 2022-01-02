import random
import math
import arcade
from base_view import BaseView

from typing import cast
from arcade.experimental.shadertoy import Shadertoy

from asteroids.constants import *
from asteroids.asteroid_sprite import AsteroidSprite
from asteroids.ship_sprite import ShipSprite
from asteroids.bullet import Bullet
from asteroids.glow_line import GlowLine
from asteroids.glow_ball import GlowBall
from asteroids.explosion import ExplosionMaker
from asteroids.glow_image_sprite import GlowImageSprite


class AsteroidsView(BaseView):
    """ Main application class. """

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        self.total_time = 0
        self.frame_count = 0

        self.game_over = False

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()

        # Sounds
        self.laser_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound1 = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.hit_sound2 = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.hit_sound3 = arcade.load_sound(":resources:sounds/hit1.wav")
        self.hit_sound4 = arcade.load_sound(":resources:sounds/hit2.wav")

        self.glowball_shadertoy = Shadertoy.create_from_file(self.window.get_size(), "asteroids/glow_ball.glsl")
        self.glowline_shadertoy = Shadertoy.create_from_file(self.window.get_size(), "asteroids/glow_line.glsl")

        self.explosion_list = []

    def start_new_game(self, player_count):
        """ Set up the game and initialize the variables. """

        self.game_over = False
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()

        joystick = None

        player_sprite = ShipSprite(":resources:images/space_shooter/playerShip1_orange.png",
                                   SCALE,
                                   joystick,
                                   player_no=1,
                                   player_count=player_count)
        self.player_sprite_list.append(player_sprite)
        player_sprite.center_x = 300
        player_sprite.center_y = 300
        player_sprite.angle = 270

        player_sprite = ShipSprite(":resources:images/space_shooter/playerShip1_green.png",
                                   SCALE,
                                   joystick,
                                   player_no=2,
                                   player_count=player_count
                                   )
        self.player_sprite_list.append(player_sprite)
        player_sprite.center_x = 300
        player_sprite.center_y = 600
        player_sprite.angle = 270

        # Set up the player
        for player in self.player_sprite_list:
            player.score = 0
            player.lives = 3

        # Set up the little icons that represent the player lives.
        cur_pos = 10
        for i in range(self.player_sprite_list[0].lives):
            life = arcade.Sprite(":resources:images/space_shooter/playerLife1_orange.png", SCALE)
            life.center_x = cur_pos + life.width
            life.center_y = life.height
            cur_pos += life.width
            self.ship_life_list.append(life)

        if len(self.player_sprite_list) > 1:
            cur_pos = 100
            for i in range(self.player_sprite_list[1].lives):
                life = arcade.Sprite(":resources:images/space_shooter/playerLife1_green.png", SCALE)
                life.center_x = cur_pos + life.width
                life.center_y = life.height
                cur_pos += life.width
                self.ship_life_list.append(life)

        # Make the asteroids
        image_list = (":resources:images/space_shooter/meteorGrey_big1.png",
                      ":resources:images/space_shooter/meteorGrey_big2.png",
                      ":resources:images/space_shooter/meteorGrey_big3.png",
                      ":resources:images/space_shooter/meteorGrey_big4.png")
        for player_sprite in self.player_sprite_list:

            image_no = random.randrange(4)
            enemy_sprite = AsteroidSprite(image_list[image_no], SCALE)
            enemy_sprite.guid = "Asteroid"

            enemy_sprite.center_y = player_sprite.center_y
            enemy_sprite.center_x = 1100 + random.randrange(0, 300)

            enemy_sprite.change_x = random.random() * 1 - 0.5
            enemy_sprite.change_y = random.random() * 0.5 - 0.25

            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            self.asteroid_list.append(enemy_sprite)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.asteroid_list.draw()
        self.ship_life_list.draw()

        for bullet in self.bullet_list:
            bullet.draw()

        self.bullet_list.draw()
        for explosion in self.explosion_list:
            explosion.render()

        self.player_sprite_list.draw()

        # Put the text on the screen.

        output = f"Player 1 Score: {self.player_sprite_list[0].score}"
        arcade.draw_text(output, 10, 40, arcade.color.AMBER,
                         font_size=35,
                         font_name="Arcade")

        if len(self.player_sprite_list) > 1:
            output = f"Player 2 Score: {self.player_sprite_list[1].score}"
            arcade.draw_text(output, 500, 40, arcade.color.AMBER,
                             font_size=35,
                             font_name="Arcade")

        output = f"Asteroid Count: {len(self.asteroid_list)}"
        arcade.draw_text(output, 10, 80, arcade.color.AMBER,
                         font_size=35,
                         font_name="Arcade")

        self.draw_line_one("Use Shaders for glow effects and explosions")

    def fire_circle(self, bullet_color, player_sprite, player_no):
        bullet_sprite = GlowBall(glowcolor=bullet_color,
                                 radius=5,
                                 shadertoy=self.glowball_shadertoy,
                                 player_no=player_no)
        self.set_bullet_vector(bullet_sprite, 5, player_sprite)
        arcade.play_sound(self.laser_sound)

    def fire_line(self, bullet_color, player_sprite, player_no):
        bullet_sprite = GlowLine(glowcolor=bullet_color,
                                 shadertoy=self.glowline_shadertoy,
                                 player=player_sprite,
                                 player_no=player_no)
        self.set_bullet_vector(bullet_sprite, 13, player_sprite)
        arcade.play_sound(self.laser_sound)

    def set_bullet_vector(self, bullet_sprite, bullet_speed, player_sprite):
        bullet_sprite.change_y = \
            math.cos(math.radians(player_sprite.angle)) * bullet_speed
        bullet_sprite.change_x = \
            -math.sin(math.radians(player_sprite.angle)) \
            * bullet_speed

        bullet_sprite.center_x = player_sprite.center_x
        bullet_sprite.center_y = player_sprite.center_y

        self.bullet_list.append(bullet_sprite)

    def split_asteroid(self, asteroid: AsteroidSprite):
        """ Split an asteroid into chunks. """
        x = asteroid.center_x
        y = asteroid.center_y

        if asteroid.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                              ":resources:images/space_shooter/meteorGrey_med2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound1.play()

        elif asteroid.size == 3:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_small1.png",
                              ":resources:images/space_shooter/meteorGrey_small2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound2.play()

        elif asteroid.size == 2:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_tiny1.png",
                              ":resources:images/space_shooter/meteorGrey_tiny2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound3.play()

        elif asteroid.size == 1:
            self.hit_sound4.play()

    def on_update(self, delta_time):
        """ Move everything """

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)

        self.frame_count += 1

        if self.frame_count == 15:
            self.fire_circle(arcade.color.RED, self.player_sprite_list[0], 1)

        if self.frame_count == 30:
            self.fire_line(arcade.color.PURPLE, self.player_sprite_list[1], 2)

        self.asteroid_list.update()
        self.bullet_list.update()
        self.player_sprite_list.update()
        explosion_list_copy = self.explosion_list.copy()
        for explosion in explosion_list_copy:
            explosion.update(delta_time)
            if explosion.time > .9:
                self.explosion_list.remove(explosion)

        for bullet in self.bullet_list:
            assert isinstance(bullet, Bullet)
            asteroids = arcade.check_for_collision_with_list(bullet, self.asteroid_list)

            if len(asteroids) > 0:
                explosion = ExplosionMaker(self.window.get_size(), bullet.position)
                self.explosion_list.append(explosion)

            for asteroid in asteroids:
                assert isinstance(asteroid, AsteroidSprite)
                self.player_sprite_list[bullet.player_no - 1].score += 1

                self.split_asteroid(cast(AsteroidSprite, asteroid))  # expected AsteroidSprite, got Sprite instead
                asteroid.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

            # Remove bullet if it goes off-screen
            size = max(bullet.width, bullet.height)
            if bullet.center_x < 0 - size:
                bullet.remove_from_sprite_lists()
            if bullet.center_x > SCREEN_WIDTH + size:
                bullet.remove_from_sprite_lists()
            if bullet.center_y < 0 - size:
                bullet.remove_from_sprite_lists()
            if bullet.center_y > SCREEN_HEIGHT + size:
                bullet.remove_from_sprite_lists()

        for player in self.player_sprite_list:
            assert isinstance(player, ShipSprite)
            if not player.respawning:
                asteroids = arcade.check_for_collision_with_list(player, self.asteroid_list)
                if len(asteroids) > 0:
                    if player.lives > 0:
                        player.lives -= 1
                        player.respawn()
                        self.split_asteroid(cast(AsteroidSprite, asteroids[0]))
                        asteroids[0].remove_from_sprite_lists()
                        self.ship_life_list.pop().remove_from_sprite_lists()
                        print("Crash")
                    else:
                        self.game_over = True
                        print("Game over")
