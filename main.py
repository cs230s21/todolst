import kivysome

from kivy.app import App
from kivy.config import Config
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from libs.get_data import get_user_data, get_theme_palette
from libs.data_handler import ProcessTaskHandler
from screens.upcoming_route import UpcomingRoute
from screens.add_task_route import AddTaskRoute
from screens.completed_route import CompletedRoute
from screens.theme_route import ThemeRoute

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')
# Config.set('graphics', 'width', '450')
# Config.set('graphics', 'height', '900')

kivysome.enable("https://kit.fontawesome.com/4adb19bb6e.js",
                group=kivysome.FontGroup.SOLID, font_folder="assets/fonts")

Builder.load_file('libs/custom_kv_widget.kv')
Builder.load_file('screens/upcoming_route.kv')
Builder.load_file('screens/add_task_route.kv')
# Builder.load_file('screens/add_task_route2.kv')
Builder.load_file('screens/completed_route.kv')
Builder.load_file('screens/theme_route.kv')


class MyApp(App):
    user_data = get_user_data()
    theme_palette = get_theme_palette(user_data['theme_name'])
    route_manager = ScreenManager()

    def process_task_handler(self, _to, task, date=None):
        ProcessTaskHandler(app=self, _to=_to, task=task, _date=date)

    def build(self):
        self.route_manager.add_widget(UpcomingRoute(app=self))
        self.route_manager.add_widget(AddTaskRoute(app=self))
        self.route_manager.add_widget(CompletedRoute(app=self))
        self.route_manager.add_widget(ThemeRoute(app=self))

        self.route_manager.return_route = ''
        return self.route_manager

    def on_stop(self):
        self.process_task_handler(_to='save_file', task='')

    def refresh_theme(self):
        Builder.unload_file('libs/custom_kv_widget.kv')
        Builder.unload_file('screens/upcoming_route.kv')
        Builder.unload_file('screens/add_task_route.kv')
        Builder.unload_file('screens/completed_route.kv')
        Builder.unload_file('screens/theme_route.kv')

        Builder.load_file('libs/custom_kv_widget.kv')
        Builder.load_file('screens/upcoming_route.kv')
        Builder.load_file('screens/add_task_route.kv')
        Builder.load_file('screens/completed_route.kv')
        Builder.load_file('screens/theme_route.kv')
        self.route_manager.clear_widgets()
        self.route_manager.add_widget(ThemeRoute(app=self))
        self.route_manager.add_widget(UpcomingRoute(app=self))
        self.route_manager.add_widget(AddTaskRoute(app=self))
        self.route_manager.add_widget(CompletedRoute(app=self))


if __name__ == '__main__':
    MyApp().run()
