from kivysome import icon
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from libs.get_data import get_theme_palette

"""
screen_4.py

Functions used by WindowFour in screens_setups.py can be found here.
"""


class ThemeLayout(BoxLayout):
    def __init__(self, root, theme_name, theme_dict, **kwargs):
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
        if self.collide_point(*touch.pos):
            self.ids.overlay.opacity = 0.5

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.collide_point(*touch.opos):
            if self.root.app.user_data['theme_name'] != self.theme_name:
                self.root.change_theme(self.theme_name)
        self.ids.overlay.opacity = 1


class ThemeRoute(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.normal_theme = get_theme_palette("todolst")
        self.dark_theme = get_theme_palette("dark")
        self.themes = ['todolst', 'dark', 'neutral']

    def add_theme_choice(self, theme_name, theme_dict, chosen):
        theme_choice = ThemeLayout(self, theme_name, theme_dict)
        if chosen:
            theme_choice.ids.choice_checkbox.text = "%s" % icon('check')
        self.ids.themes.add_widget(theme_choice)

    def on_pre_enter(self, *args):
        for theme in self.themes:
            chosen = self.app.user_data['theme_name'] == theme
            self.add_theme_choice(theme, get_theme_palette(theme), chosen)

    def on_leave(self, *args):
        self.ids.themes.clear_widgets()

    def change_theme(self, theme_name):
        self.app.theme_palette = get_theme_palette(theme_name)
        self.app.user_data['theme_name'] = theme_name
        self.app.refresh_theme()
