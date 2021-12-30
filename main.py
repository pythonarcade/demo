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
        view = StartView()
        self.view_list.append(view)

        from draw_sprites.draw_sprites import DrawSprites
        view = DrawSprites()
        self.view_list.append(view)

        from rotate_sprites.rotate_sprites import RotateSprites
        view = RotateSprites()
        self.view_list.append(view)

        from scale_sprites.scale_sprites import ScaleSprites
        view = ScaleSprites()
        self.view_list.append(view)


def main():
    """ Main function """

    window = DemoWindow()
    window.center_window()
    window.create_views()

    cur_view = window.view_list.pop(0)
    window.show_view(cur_view)
    arcade.run()


if __name__ == "__main__":
    main()