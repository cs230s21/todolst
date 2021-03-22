from kivysome import icon
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from libs.get_data import get_theme_palette

"""
This module contains two classes. The first one is ThemeRoute, which represents 
the screen that lets the user choose the theme for the app. The second one is
ThemeLayout, which represents the option for a theme
"""


class ThemeLayout(BoxLayout):
    """
    This class represents a theme option. There will be one object of this class
    for each theme in ../assets/theme_palettes.json.

    Extends class BoxLayout.
    """

    def __init__(self, root, theme_name, theme_dict, **kwargs):
        """
        Initialize a ThemeLayout object.

        Store the name and information of the theme the object represents, then
        initialize the color of its children.

        :param root: the layout that contains this object.
        :param theme_name: the name of theme this object represents.
        :param theme_dict: the dictionary containing the information about the
            theme this object represents.
        :param kwargs: Keyword parameters for superclass Screen.
        """
        super().__init__(**kwargs)
        self.root = root
        self.theme_name = theme_name
        self.primary_color = theme_dict['primary_color']
        self.primary_text_color = theme_dict['text_primary_color']
        self.secondary_color = theme_dict['secondary_color']
        self.secondary_text_color = theme_dict['text_secondary_color']
        self.theme_background_color = theme_dict['background_color']

        self.ids.primary_color_label_button.background_color = \
            self.primary_color
        self.ids.primary_color_label_button.color = self.primary_text_color
        self.ids.primary_color_label_button.text = theme_name
        self.ids.space_filling_label_button.background_color = \
            self.theme_background_color
        self.ids.choice_checkbox.background_color = self.theme_background_color
        self.ids.choice_checkbox.color = (0, 1, 0, 1)

    def on_touch_down(self, touch):
        """
        Apply an overlay over the object when it is clicked on to create the
        effect of it being chosen.

        Override BoxLayout.on_touch_down()

        :param touch: an object containing the data about the mouse click.
        """
        if self.collide_point(*touch.pos):
            self.ids.overlay.opacity = 0.5

    def on_touch_up(self, touch):
        """
        Makes the theme this object represents the one used in the app and
        remove the overlay over this object.

        Override BoxLayout.on_touch_up(). If this object is clicked, and the
        click is released when hovering over it, the theme it represents will be
        chosen.

        :param touch: an object containing the data about the mouse click.
        """

        if self.collide_point(*touch.pos) and self.collide_point(*touch.opos):
            if self.root.app.user_data['theme_name'] != self.theme_name:
                self.root.change_theme(self.theme_name)
        self.ids.overlay.opacity = 1


class ThemeRoute(Screen):
    """
    This class represents the screen that contain the theme options.

    Extends class Screen. This class only implements the logic portion of the
    screen it represents. The graphic portion is contained in
    completed_route.py.
    """

    def __init__(self, app, **kwargs):
        """
        Initialize a CompletedScreen object.

        Store the app that contains the screen for future use and create a list
        that stores the available themes' names.

        :param app: The app that contains this screen.
        :param kwargs: Keyword parameters for superclass Screen.
        """
        super().__init__(**kwargs)
        self.app = app
        self.themes = ['todolst', 'dark', 'neutral']

    def add_theme_choice(self, theme_name, theme_dict, chosen):
        """
        Create a ThemeLayout object associated with a theme and add it to the
        screen.

        :param theme_name: the name of the theme being added
        :param theme_dict: dictionary of the information about the theme being
            added
        :param chosen: whether the theme being added is the current theme
        """
        theme_choice = ThemeLayout(self, theme_name, theme_dict)
        if chosen:
            theme_choice.ids.choice_checkbox.text = "%s" % icon('check')
        self.ids.themes.add_widget(theme_choice)

    # Used on_pre_enter() instead of on_enter() because it runs when the screen
    # transition is happening, which eliminates the pause when entering this
    # screen
    def on_pre_enter(self, *args):
        """
        Populate the screen with the theme choices upon entry.

        Override Screen.on_pre_enter()

        :param args: Arguments used by Screen.on_pre_enter().
        """
        for theme in self.themes:
            chosen = self.app.user_data['theme_name'] == theme
            self.add_theme_choice(theme, get_theme_palette(theme), chosen)

    def on_leave(self, *args):
        """
        Clear the screen upon leaving.

        Override Screen.on_leave()

        :param args: Arguments used by Screen.on_leave().
        """
        self.ids.themes.clear_widgets()

    def change_theme(self, theme_name):
        """
        Change the theme of the app. Called when a theme option is clicked.

        :param theme_name: the name of the theme being changed to
        """
        self.app.theme_palette = get_theme_palette(theme_name)
        self.app.user_data['theme_name'] = theme_name
        self.app.refresh_theme()
