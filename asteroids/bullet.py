import arcade


class Bullet(arcade.Sprite):
    def __init__(self, image_file=None, scale=1.0, shadertoy=None, player_no=1):
        super().__init__(image_file, scale)
        self.type = None
        self.shadertoy = shadertoy
        self.player_no = player_no

    def draw(self):
        pass
