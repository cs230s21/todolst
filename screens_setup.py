"""
screens_setup.py

Functionality for all screens are implemented here from their respective
files (i.e. WindowOne uses functions from screen_1.py). Be sure to install
a virtual environment with Kivy before using.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from screen_2 import add_task_to_json, update_remaining_tasks


class WindowOne(Screen):
    pass


class WindowTwo(Screen):
    def add_task(self):
        add_task_to_json(self)

    def update_tasks(self):
        update_remaining_tasks(self)


class WindowThree(Screen):
    pass


class WindowFour(Screen):
    pass


class WindowManager(ScreenManager):
    pass


screens_kv = Builder.load_file('screens.kv')


class ScreensApp(App):
    def build(self):
        return screens_kv


if __name__ == '__main__':
    ScreensApp().run()
