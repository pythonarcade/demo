from typing import List
import arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Arcade Demo"


class DemoWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.media_player = None
        self.my_music = arcade.load_sound("music/into-battle-15601.mp3")
        arcade.enable_timings()

        self.view_list: List[arcade.View] = []

        from loading.loading import LoadingView
        view = LoadingView(3.5)
        self.view_list.append(view)
        self.show_view(view)
        self.frame_count = 0
        self.loading_view = view

    def start_music(self):
        # return
        if not self.media_player:
            # Play button has been hit, and we need to start playing from the beginning.
            self.media_player = self.my_music.play()
            self.media_player.volume = 0.1
        elif not self.media_player.playing:
            # Play button hit, and we need to un-pause our playing.
            self.media_player.play()
        elif self.media_player.playing:
            # We are playing music, so pause.
            self.media_player.pause()
            self.media_player = self.my_music.play()

    def on_update(self, delta_time: float):
        self.frame_count += 1
        if self.frame_count >= 20:
            self.create_views(self.frame_count - 20)

    def create_views(self, count):
        prototype = False

        if count == 0:
            from start.start_view import StartView
            view = StartView(4.5)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Drawing"

        elif count == 1 and not prototype:
            from draw_sprites.draw_sprites import DrawSprites
            view = DrawSprites(3.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Rotating"

        elif count == 2 and not prototype:
            from rotate_sprites.rotate_sprites import RotateSprites
            view = RotateSprites(2.5)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Scaling"

        elif count == 3 and not prototype:
            from scale_sprites.scale_sprites import ScaleSprites
            view = ScaleSprites(1.8)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Lots of sprites"

        elif count == 4 and not prototype:
            from lots_of_sprites.lots_of_sprites import LotsOfSprites
            view = LotsOfSprites(4.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Moving sprites"

        elif count == 5 and not prototype:
            from moving_sprites.moving_sprites import MovingSprites
            view = MovingSprites(4.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Hitboxes"

        elif count == 6 and not prototype:
            from hit_box.hit_boxes import HitBoxes
            view = HitBoxes(3.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Spatial hash"

        elif count == 7 and not prototype:
            from spatial_hash.spatial_hash import SpatialHashDemo
            view = SpatialHashDemo(4.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Spatial collision"

        elif count == 8 and not prototype:
            from collision_spatial.collision_spatial import CollisionSpatial
            view = CollisionSpatial(6.5)
            self.view_list.append(view)

        elif count == 9 and not prototype:
            from collision_gpu.collision_gpu import CollisionGPU
            view = CollisionGPU(6.5)
            self.view_list.append(view)
            self.loading_view.line_two_text = "GPU collision"

        elif count == 10 and not prototype:
            from camera.camera_view import CameraView
            view = CameraView(3.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Camera view"

        elif count == 11 and not prototype:
            from view_support.view_support import ViewSupport
            view = ViewSupport(4.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "GUI"

        elif count == 12 and not prototype:
            self.loading_view.line_two_text = "Tiled map"
            # from gui.gui_view import GuiView
            # view = GuiView(4.0)
            # self.view_list.append(view)

        elif count == 13 and not prototype:
            from tiled_map.tiled_map import TiledMap
            view = TiledMap(6.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Platformer"

        elif count == 14 and not prototype:
            from platformer_engine.platformer_engine import PlatformerEngine
            view = PlatformerEngine(6.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Pymunk"

        elif count == 15 and not prototype:
            from pymunk_view.pymunk_view import PymunkView
            view = PymunkView(6.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Minimap"

        elif count == 16 and not prototype:
            from minimap.minimap import Minimap
            view = Minimap(5.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Parallax"

        elif count == 17 and not prototype:
            from parallax.parallax import ParallaxView
            view = ParallaxView(4.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Raycasting"

        elif count == 18 and not prototype:
            from ray_casting.ray_casting import RayCasting
            view = RayCasting(4.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Asteroids"

        elif count == 19 and not prototype:
            from asteroids.asteroids_view import AsteroidsView
            view = AsteroidsView(5.5)
            view.start_new_game(1)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Normal mapping"

        elif count == 20 and not prototype:
            from normal_mapping.normal_mapping import NormalMapping
            view = NormalMapping(5.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Shader background"

        elif count == 21 and not prototype:
            from shader_background.shader_background import ShaderBackground
            view = ShaderBackground(3.0)
            self.view_list.append(view)

        elif count == 22 and not prototype:
            from compute_shader.compute_shader import ComputeShader
            view = ComputeShader(6.0)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Compute shader"

        elif count == 23 and not prototype:
            from feature_list.feature_list import FeatureListView
            t = ["Python 3.7+",
                 "Open Source",
                 "MIT Licensed",
                 "Modern OpenGL pipeline",
                 "Fully typed",
                 "Built on Pyglet",]
            view = FeatureListView(6, t)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Drawing"

        elif count == 24 and not prototype:
            from feature_list.feature_list import FeatureListView
            t = ["Detailed documentation",
                 "100+ Example programs",
                 "6+ years of releases",
                 "1400+ stars on GitHub",
                 "Active Discord Community"]
            view = FeatureListView(6, t)
            self.view_list.append(view)
            self.loading_view.line_two_text = "Drawing"
        elif count == 23 and not prototype:
            from shader_background.shader_background import ShaderBackground
            view = ShaderBackground(10.0, True)
            self.view_list.append(view)

        elif count == 25:
            from end_slide.end_slide import EndSlide
            view = EndSlide(10.0)
            self.view_list.append(view)

            self.start_music()


def main():
    """ Main function """

    arcade.load_font("fonts/CabinSketch-Bold.ttf")
    window = DemoWindow()
    window.center_window()

    cur_view = window.view_list.pop(0)
    window.show_view(cur_view)
    arcade.run()


if __name__ == "__main__":
    main()
