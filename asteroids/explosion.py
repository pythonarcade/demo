from arcade.experimental.shadertoy import Shadertoy


class ExplosionMaker:
    def __init__(self, size, position):
        self.shadertoy: Shadertoy = Shadertoy.create_from_file(size, "asteroids/explosion.glsl")
        self.shadertoy.program['explosionPos'] = position
        self.time = 0.0
        self.position = position

    def update(self, time):
        self.time += time

    def render(self):
        self.shadertoy.render(time=self.time)
