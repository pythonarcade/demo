import arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Arcade Demo"


class DemoWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.view_list = []

    def create_views(self):
        self.view_list = []

        from start.start_view import StartView
        view = StartView(3.0)
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
        view = LotsOfSprites(3.0)
        self.view_list.append(view)

        from hit_box.hit_boxes import HitBoxes
        view = HitBoxes(3.0)
        self.view_list.append(view)

        from ray_casting.ray_casting import RayCasting
        view = RayCasting(4.0)
        self.view_list.append(view)

        from asteroids.asteroids_view import AsteroidsView
        view = AsteroidsView(5.5)
        view.start_new_game(1)
        self.view_list.append(view)

        from shader_background.shader_background import ShaderBackground
        view = ShaderBackground(3.0)
        self.view_list.append(view)

        from compute_shader.compute_shader import ComputeShader
        view = ComputeShader(6.0)
        self.view_list.append(view)


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