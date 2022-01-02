"""
Compute shader with buffers
"""
import random
import math
from array import array

import arcade
from arcade.gl import BufferDescription
from base_view import BaseView

# Window dimensions
WINDOW_WIDTH = 2300
WINDOW_HEIGHT = 1300

# Size of performance graphs
GRAPH_WIDTH = 200
GRAPH_HEIGHT = 120
GRAPH_MARGIN = 5

STARFIELD_RADIUS = 275


class ComputeShader(BaseView):

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        # --- Class instance variables

        # Number of balls to move
        self.num_stars = 60000

        # This has something to do with how we break the calculations up
        # and parallelize them.
        self.group_x = 256
        self.group_y = 1

        # --- Create buffers

        # Format of the buffer data.
        # 4f = position and size -> x, y, z, radius
        # 4x4 = Four floats used for calculating velocity. Not needed for visualization.
        # 4f = color -> rgba
        buffer_format = "4f 4x4 4f"
        # Generate the initial data that we will put in buffer 1.
        # Pick one of these or make your own function
        # initial_data = self.gen_random_space()
        initial_data = self.gen_galaxies_colliding()

        # Create data buffers for the compute shader
        # We ping-pong render between these two buffers
        # ssbo = shader storage buffer object
        self.ssbo_1 = self.window.ctx.buffer(data=array('f', initial_data))
        self.ssbo_2 = self.window.ctx.buffer(reserve=self.ssbo_1.size)

        # Attribute variable names for the vertex shader
        attributes = ["in_vertex", "in_color"]
        self.vao_1 = self.window.ctx.geometry(
            [BufferDescription(self.ssbo_1, buffer_format, attributes)],
            mode=self.window.ctx.POINTS,
        )
        self.vao_2 = self.window.ctx.geometry(
            [BufferDescription(self.ssbo_2, buffer_format, attributes)],
            mode=self.window.ctx.POINTS,
        )

        # --- Create shaders

        # Load in the shader source code
        file = open("compute_shader/compute_shader.glsl")
        compute_shader_source = file.read()
        file = open("compute_shader/vertex_shader.glsl")
        vertex_shader_source = file.read()
        file = open("compute_shader/fragment_shader.glsl")
        fragment_shader_source = file.read()
        file = open("compute_shader/geometry_shader.glsl")
        geometry_shader_source = file.read()

        # Create our compute shader.
        # Search/replace to set up our compute groups
        compute_shader_source = compute_shader_source.replace("COMPUTE_SIZE_X",
                                                              str(self.group_x))
        compute_shader_source = compute_shader_source.replace("COMPUTE_SIZE_Y",
                                                              str(self.group_y))
        self.compute_shader = self.window.ctx.compute_shader(source=compute_shader_source)

        # Program for visualizing the balls
        self.program = self.window.ctx.program(
            vertex_shader=vertex_shader_source,
            geometry_shader=geometry_shader_source,
            fragment_shader=fragment_shader_source,
        )

    def on_draw(self):
        # Clear the screen
        self.window.clear()
        # Enable blending so our alpha channel works
        self.window.ctx.enable(self.window.ctx.BLEND)

        # Bind buffers
        self.ssbo_1.bind_to_storage_buffer(binding=0)
        self.ssbo_2.bind_to_storage_buffer(binding=1)

        # Set input variables for compute shader
        # These are examples, although this example doesn't use them
        # self.compute_shader["screen_size"] = self.get_size()
        # self.compute_shader["force"] = force
        # self.compute_shader["frame_time"] = self.run_time

        # Run compute shader
        self.compute_shader.run(group_x=self.group_x, group_y=self.group_y)

        # Draw the balls
        self.vao_2.render(self.program)

        # Swap the buffers around (we are ping-ping rendering between two buffers)
        self.ssbo_1, self.ssbo_2 = self.ssbo_2, self.ssbo_1
        # Swap what geometry we draw
        self.vao_1, self.vao_2 = self.vao_2, self.vao_1

        self.draw_line_one("Compute Shader for GPU based computations")

    def gen_galaxies_colliding(self):
        radius = 3.0
        for i in range(self.num_stars):
            # Position/radius
            angle = random.random() * math.pi * 2
            angle2 = random.random() * math.pi * 2
            distance = random.random() * STARFIELD_RADIUS

            # Alternate stars between galaxies
            if i % 2 == 0:
                yield distance * math.cos(angle) + WINDOW_WIDTH / 3 - STARFIELD_RADIUS
            else:
                yield distance * math.cos(angle) + WINDOW_WIDTH * 2 / 3 - STARFIELD_RADIUS
            yield distance * math.sin(angle) + WINDOW_HEIGHT / 4
            yield distance * math.sin(angle2)
            yield radius

            # Velocity
            yield math.cos(angle + math.pi / 2) * distance / 100
            yield math.sin(angle + math.pi / 2) * distance / 100
            yield math.sin(angle2 + math.pi / 2) * distance / 100
            yield 0.0  # vw (padding)

            # Color
            if i % 2 == 0:
                yield 1.0  # r
                yield 1.0  # g
                yield 0.5  # b
            else:
                yield 1.0  # r
                yield 0.5  # g
                yield 1.0  # b
            yield 1.0  # a

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)
