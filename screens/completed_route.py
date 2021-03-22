"""
This module contains the class CompletedRoute, which represents the screen that
contains the completed tasks.
"""

from kivy.uix.screenmanager import Screen
from libs.custom_kv_widget import TaskView


class CompletedRoute(Screen):
    """
    This class represents the screen that contain the completed tasks.

    Extends class Screen.
    """

    def __init__(self, app, **kwargs):
        """
        Initialize a CompletedRoute object.

        Store the app that contains the screen for future use and create a local
        copy of the completed tasks data.

        :param app: The app that contains this screen.
        :param kwargs: Keyword parameters for superclass Screen.
        """
        super().__init__(**kwargs)
        self.app = app
        self.completed_tasks = self.app.user_data['completed']

    # Used on_pre_enter instead of on_enter because it runs when the screen
    # transition is happening, which eliminates the pause when entering this
    # screen
    def on_pre_enter(self, *args):
        """
        Populate the screen with the completed tasks upon entry.

        Override Screen.on_pre_enter()

        :param args: Arguments used by Screen.on_pre_enter().
        """
        self.populate_tasks()

    def on_leave(self):
        """
        Clear the screen upon leaving.

        Override Screen.on_leave()
        """
        self.ids.completed_tasks.clear_widgets()

    def remove_tasks_completed_more_than_24_hours_ago(self):
        """
        Helper method to remove tasks that are more than 24 hours.
        """
        self.app.process_task_handler('update_completed', '')

    def remove_task(self, task_id, task_view):
        """
        Remove a task from the screen and the data.

        :param task_id: the id of the task to be deleted
        :param task_view: the widget that displays the completed tasks
        """
        for task in self.completed_tasks:
            if task['id'] == task_id:
                self.app.process_task_handler('upcoming', task)
                self.completed_tasks.remove(task)
                break

        self.ids.completed_tasks.remove_widget(task_view)

    def populate_tasks(self):
        """
        Populate the screen with the completed tasks. Will first remove the
        tasks that are completed more than 24 hours ago.
        """
        self.remove_tasks_completed_more_than_24_hours_ago()

        for task in self.completed_tasks:
            row = TaskView(self, task, checkbox_active=True)
            self.ids.completed_tasks.add_widget(row)
