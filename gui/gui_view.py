"""
Example code showing how to create some of the
different UIWidgets.
"""
import arcade
import arcade.gui
from base_view import BaseView


class GuiView(BaseView):

    def __init__(self, time_on_screen):
        super().__init__(time_on_screen)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create a text label
        ui_text_label = arcade.gui.UITextArea(text="This is a Text Widget",
                                              width=500,
                                              height=40,
                                              font_size=24,
                                              font_name="Kenney Future")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        text = "The real danger is not that computers will begin to think like people, " \
               "but that people will begin " \
               "to think like computers. - Sydney Harris (Journalist)"
        ui_text_label = arcade.gui.UITextArea(text=text,
                                              width=500,
                                              height=60,
                                              font_size=12,
                                              font_name="Arial")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        # Create a UIFlatButton
        ui_flatbutton = arcade.gui.UIFlatButton(text="Instructions", width=200)
        self.v_box.add(ui_flatbutton.with_space_around(bottom=20))

        # Create a UIFlatButton
        ui_flatbutton = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(ui_flatbutton.with_space_around(bottom=20))

        # Create a UIFlatButton
        ui_flatbutton = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.v_box.add(ui_flatbutton.with_space_around(bottom=20))

        # Handle Clicks
        @ui_flatbutton.event("on_click")
        def on_click_flatbutton(event):
            print("UIFlatButton pressed", event)

        # Create a UITextureButton
        texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/play.png")
        ui_texture_button = arcade.gui.UITextureButton(texture=texture)

        # Handle Clicks
        @ui_texture_button.event("on_click")
        def on_click_texture_button(event):
            print("UITextureButton pressed", event)

        self.v_box.add(ui_texture_button.with_space_around(bottom=20))

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box)
        )

    def on_click_start(self, event):
        print("Start:", event)

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
        self.draw_line_one("GUI Controls")

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views()

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)