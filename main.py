import arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Arcade Demo"


class DemoWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.view_list = []
        self.media_player = None
        self.my_music = arcade.load_sound("music/into-battle-15601.mp3")
        arcade.enable_timings()

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

    def create_views(self):
        self.view_list = []

        from start.start_view import StartView
        view = StartView(3.5)
        self.view_list.append(view)

        from draw_sprites.draw_sprites import DrawSprites
        view = DrawSprites(3.0)
        self.view_list.append(view)

        from rotate_sprites.rotate_sprites import RotateSprites
        view = RotateSprites(2.5)
        self.view_list.append(view)

        from scale_sprites.scale_sprites import ScaleSprites
        view = ScaleSprites(1.8)
        self.view_list.append(view)

        from lots_of_sprites.lots_of_sprites import LotsOfSprites
        view = LotsOfSprites(4.0)
        self.view_list.append(view)

        from moving_sprites.moving_sprites import MovingSprites
        view = MovingSprites(4.0)
        self.view_list.append(view)

        from hit_box.hit_boxes import HitBoxes
        view = HitBoxes(3.0)
        self.view_list.append(view)

        from spatial_hash.spatial_hash import SpatialHashDemo
        view = SpatialHashDemo(4.0)
        self.view_list.append(view)

        from collision_spatial.collision_spatial import CollisionSpatial
        view = CollisionSpatial(6.5)
        self.view_list.append(view)

        from collision_gpu.collision_gpu import CollisionGPU
        view = CollisionGPU(6.5)
        self.view_list.append(view)

        from camera.camera_view import CameraView
        view = CameraView(3.0)
        self.view_list.append(view)

        from view_support.view_support import ViewSupport
        view = ViewSupport(4.0)
        self.view_list.append(view)

        # from gui.gui_view import GuiView
        # view = GuiView(4.0)
        # self.view_list.append(view)

        from tiled_map.tiled_map import TiledMap
        view = TiledMap(6.0)
        self.view_list.append(view)

        from platformer_engine.platformer_engine import PlatformerEngine
        view = PlatformerEngine(6.0)
        self.view_list.append(view)

        from pymunk_view.pymunk_view import PymunkView
        view = PymunkView(6.0)
        self.view_list.append(view)

        from minimap.minimap import Minimap
        view = Minimap(5.0)
        self.view_list.append(view)

        from parallax.parallax import ParallaxView
        view = ParallaxView(4.0)
        self.view_list.append(view)

        from ray_casting.ray_casting import RayCasting
        view = RayCasting(4.0)
        self.view_list.append(view)

        from asteroids.asteroids_view import AsteroidsView
        view = AsteroidsView(5.5)
        view.start_new_game(1)
        self.view_list.append(view)

        from normal_mapping.normal_mapping import NormalMapping
        view = NormalMapping(5.0)
        self.view_list.append(view)

        from shader_background.shader_background import ShaderBackground
        view = ShaderBackground(3.0)
        self.view_list.append(view)

        from compute_shader.compute_shader import ComputeShader
        view = ComputeShader(6.0)
        self.view_list.append(view)

        from end_slide.end_slide import EndSlide
        view = EndSlide(10.0)
        self.view_list.append(view)

        self.start_music()


def main():
    """ Main function """

    arcade.load_font("fonts/CabinSketch-Bold.ttf")
    window = DemoWindow()
    window.center_window()
    window.create_views()

    cur_view = window.view_list.pop(0)
    window.show_view(cur_view)
    arcade.run()


if __name__ == "__main__":
    main()
