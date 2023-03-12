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
        
        self.count = 0
        self.manager = arcade.gui.UIManager()

        self.resume_button = arcade.gui.UIFlatButton(text="Resume", width=150)
        start_new_game_button = arcade.gui.UIFlatButton(text="Start New Game", width=150)
        volume_button = arcade.gui.UIFlatButton(text="Volume", width=150)
        self.options_button = arcade.gui.UIFlatButton(text="Options", width=150)
        self.options_menu = None

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=320)

        # Initialise a grid in which widgets can be arranged.
        self.grid = arcade.gui.UIGridLayout(column_count=2, row_count=3, horizontal_spacing=20, vertical_spacing=20)

        # Adding the buttons to the layout.
        self.grid.add(self.resume_button, col_num=0, row_num=0)
        self.grid.add(start_new_game_button, col_num=1, row_num=0)
        self.grid.add(volume_button, col_num=0, row_num=1)
        self.grid.add(self.options_button, col_num=1, row_num=1)
        self.grid.add(exit_button, col_num=0, row_num=2, col_span=2)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        @volume_button.event("on_click")
        def on_click_volume_button(event):
            self.volume_menu = SubMenu(
                "Volume Menu", "How do you like your volume?", "Enable Sound",
                ["Play: Rock", "Play: Punk", "Play: Pop"],
                "Adjust Volume",
            )
            self.manager.add(
                self.volume_menu,
                layer=1
            )

        @self.options_button.event("on_click")
        def on_click_options_button(event):
            self.options_menu = SubMenu(
                "Funny Menu", "Too much fun here", "Fun?",
                ["Make Fun", "Enjoy Fun", "Like Fun"],
                "Adjust Fun"
            )
            self.manager.add(
                self.options_menu,
                layer=1
            )

    def on_click_start(self, event):
        print("Start:", event)

    def on_draw(self):
        self.clear()
        self.draw_line_one("GUI Menu")
        self.manager.draw()

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.total_time > self.time_on_screen:

            if not self.window.view_list:
                self.window.create_views(13)

            new_view = self.window.view_list.pop(0)
            self.window.show_view(new_view)
        elif self.total_time > 0.3 and self.count == 0:
            self.options_button.hovered = True
            self.count += 1
        elif self.total_time > 0.35 and self.count == 1:
            self.options_button.hovered = False
            self.options_button.pressed = True
            self.count += 1
        elif self.total_time > 0.4 and self.count == 2:
            self.options_button.pressed = False
            self.options_button.dispatch_event(
                "on_click",
                arcade.gui.UIOnClickEvent(self.options_button, self.options_button.x, self.options_button.y)
            )
            self.count += 1
        elif self.total_time > 4.95 and self.count == 21:
            self.resume_button.pressed = True

        if not hasattr(self.options_menu, "dispatch_event"):
                return

        if self.total_time > 0.75 and self.count == 3:
            self.options_menu.dispatch_event("on_update", 1)
            self.count += 1
        elif self.total_time > 0.85 and self.count == 4:
            self.options_menu.dispatch_event("on_update", 2)
            self.count += 1
        elif self.total_time > 1 and self.count == 5:
            self.options_menu.dispatch_event("on_update", 2)
            self.count += 1
        elif self.total_time > 1.25 and self.count == 6:
            self.options_menu.dispatch_event("on_update", 3)
            self.count += 1
        elif self.total_time > 2 and self.count == 7:
            self.options_menu.dispatch_event("on_update", 3)
            self.count += 1
        elif self.total_time > 2.25 and self.count == 8:
            self.options_menu.dispatch_event("on_update", 4)
            self.count += 1
        elif self.total_time > 2.85 and self.count == 9:
            self.options_menu.dispatch_event("on_update", 12)
            self.count += 1
        elif self.total_time > 3.0 and self.count == 10:
            self.options_menu.dispatch_event("on_update", 5)
            self.count += 1
        elif self.total_time > 3.25 and self.count == 11:
            self.options_menu.dispatch_event("on_update", 6)
            self.count += 1
        elif self.total_time > 3.35 and self.count == 12:
            self.options_menu.dispatch_event("on_update", 6)
            self.count += 1
        elif self.total_time > 3.45 and self.count == 13:
            self.options_menu.dispatch_event("on_update", 6)
            self.count += 1
        elif self.total_time > 3.55 and self.count == 14:
            self.options_menu.dispatch_event("on_update", 7)
            self.count += 1
        elif self.total_time > 3.65 and self.count == 15:
            self.options_menu.dispatch_event("on_update", 7)
            self.count += 1
        elif self.total_time > 3.75 and self.count == 16:
            self.options_menu.dispatch_event("on_update", 7)
            self.count += 1
        elif self.total_time > 3.85 and self.count == 17:
            self.options_menu.dispatch_event("on_update", 8)
            self.count += 1
        elif self.total_time > 4.2 and self.count == 18:
            self.options_menu.dispatch_event("on_update", 9)
            self.count += 1
        elif self.total_time > 4.5 and self.count == 19:
            self.options_menu.dispatch_event("on_update", 10)
            self.count += 1
        elif self.total_time > 4.75 and self.count == 20:
            self.options_menu.dispatch_event("on_update", 11)
            self.count += 1



class SubMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):
    """Acts like a fake view/window."""

    def __init__(self,
        title: str,
        input_text: str,
        toggle_label: str,
        dropdown_options: list[str],
        slider_label: str,
        **kwargs
    ):
        super().__init__(size_hint=(1, 1), **kwargs)

        # Setup frame which will act like the window.
        frame = self.add(arcade.gui.UIAnchorLayout(width=300, height=getattr(kwargs, "height", 400), size_hint=None))
        frame.with_padding(all=20)

        # Add a background to the window.
        # Nine patch smoothes the edges.
        frame.with_background(texture=arcade.gui.NinePatchTexture(
            left=7,
            right=7,
            bottom=7,
            top=7,
            texture=arcade.load_texture(
                "dark_blue_gray_panel.png"
            )
        ))

        self.back_button = arcade.gui.UIFlatButton(text="Back", width=250)
        # The type of event listener we used earlier for the button will not work here.
        self.back_button.on_click = self.on_click_back_button

        title_label = arcade.gui.UILabel(text=title, align="center", font_size=20, multiline=False)
        # Adding some extra space around the title.
        title_label_space = arcade.gui.UISpace(height=30, color=arcade.color.DARK_BLUE_GRAY)

        self.input_text = arcade.gui.UIInputText(text=input_text, width=250).with_border()

        # Load the on-off textures.
        on_texture = arcade.load_texture("circle_switch_on.png")
        off_texture = arcade.load_texture("circle_switch_off.png")

        # Create the on-off toggle and a label
        toggle_label = arcade.gui.UILabel(text=toggle_label)
        self.toggle = arcade.gui.UITextureToggle(
            on_texture=on_texture,
            off_texture=off_texture,
            width=20,
            height=20
        )

        # Align toggle and label horizontally next to each other
        toggle_group = arcade.gui.UIBoxLayout(vertical=False, space_between=5)
        toggle_group.add(self.toggle)
        toggle_group.add(toggle_label)

        # Create dropdown with a specified default.
        self.dropdown = arcade.gui.UIDropdown(default=dropdown_options[0], options=dropdown_options, height=20, width=250)

        slider_label = arcade.gui.UILabel(text=slider_label)
        pressed_style = arcade.gui.UISlider.UIStyle(filled_bar=arcade.color.GREEN, unfilled_bar=arcade.color.RED)
        default_style = arcade.gui.UISlider.UIStyle()
        style_dict = {"press": pressed_style, "normal": default_style, "hover": default_style, "disabled": default_style}
        # Configuring the styles is optional.
        self.slider = arcade.gui.UISlider(value=50, width=250, style=style_dict)

        widget_layout = arcade.gui.UIBoxLayout(align="left", space_between=10)
        widget_layout.add(title_label)
        widget_layout.add(title_label_space)
        widget_layout.add(self.input_text)
        widget_layout.add(toggle_group)
        widget_layout.add(self.dropdown)
        widget_layout.add(slider_label)
        widget_layout.add(self.slider)

        widget_layout.add(self.back_button)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="top")

    def on_click_back_button(self, event):
        # Removes the widget from the manager.
        # After this the manager will respond to its events like it previously did.
        self.parent.remove(self)


    def on_update(self, event_number):
        match event_number:
            case 1:
                self.input_text.dispatch_event(
                    "on_event",
                    arcade.gui.UIMousePressEvent(
                        self.input_text,
                        self.input_text.x + 1,
                        self.input_text.y + 1,
                        0,
                        0,
                    )
                )
            case 2:
                self.input_text.dispatch_event(
                    "on_event",
                    arcade.gui.UITextEvent(
                        self.input_text,
                        "?",
                    )
                )
            case 3:
                self.toggle.value = not self.toggle.value
            case 4:
                self.dropdown._show_overlay()
            case 5:
                child = self.dropdown._layout._children[1].child
                child.dispatch_event(
                    "on_click",
                    arcade.gui.UIOnClickEvent(child, child.x, child.y)
                )
            case 6:
                self.slider.pressed = True
                self.slider.dispatch_event(
                    "on_event",
                    arcade.gui.UIMouseDragEvent(self.slider, self.slider.value_x + 20, 0, 0, 0, 0, 0)
                )
            case 7:
                self.slider.pressed = True
                self.slider.dispatch_event(
                    "on_event",
                    arcade.gui.UIMouseDragEvent(self.slider, self.slider.value_x - 25, 0, 0, 0, 0, 0)
                )
            case 8:
                self.slider.pressed = False
            case 9:
                self.back_button.hovered = True
            case 10:
                self.back_button.hovered = False
                self.back_button.pressed = True
            case 11:
                self.back_button.pressed = False
                self.on_click_back_button(arcade.gui.UIOnClickEvent(self.back_button, 0, 0))
            case 12:
                child = self.dropdown._layout._children[1].child
                child.pressed = True
