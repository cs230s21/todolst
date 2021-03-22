import calendar

from kivy.uix.screenmanager import Screen

from libs.get_data import get_next7dates
from libs.custom_kv_widget import DateButton, DateDividerLabel, TaskView


class UpcomingRoute(Screen):
    """
    upcoming screen use to display upcoming tasks
    """
    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        """
        super().__init__(**kwargs)
        self.app = app

        # obj python pass by ref -> edit app data within class
        self.upcoming_tasks = app.user_data['upcoming']

    def on_pre_enter(self, *args):
        """
        function will be call when the animation to enter the screen start. it
        display all upcoming tasks
        """
        self.display_overdue_tasks()
        self.display_on_time_tasks()

    def on_leave(self, *args):
        """
        function will be call whn leaving the screen. the function will clear
        all widget in screen i.e. remove all unused widget, data
        """
        self.ids.upcoming_scrollview.clear_widgets()

    def display_overdue_tasks(self):
        """
        function as part of on_pre_enter process. function display all overdue
        upcoming tasks
        """
        overdue_tasks = self.upcoming_tasks['overdue']
        self.display_date_title(date_str_rep='Overdue')

        for date in overdue_tasks:
            for task in overdue_tasks[date]:
                self.ids.upcoming_scrollview.add_widget(
                    TaskView(self, task, due_date=date.strftime("%b %d"),
                             overdue=True))

    def display_on_time_tasks(self):
        """
        function as part of on_pre_enter process. function display all on time
        upcoming tasks in the next 7 days. if a day in the next 7 days don't
        have any task, the date for that day still show up. any task with due
        date outside of the next 7 days will not be display.
        """
        on_time_tasks = self.upcoming_tasks['on_time']
        due_date = on_time_tasks.keys()
        next_7_dates = get_next7dates()

        for date in next_7_dates:
            display_date = calendar.day_name[date.weekday()][
                           :3] + ' ' + date.strftime("%b %d")
            self.display_date_title(date_str_rep=display_date)

            if date in due_date:
                for task in on_time_tasks[date]:
                    self.ids.upcoming_scrollview.add_widget(
                        TaskView(self, task))

    def display_date_title(self, date_str_rep):
        """
        function display date title on the screen before display actual tasks
        for that date. If task is overdue, then overdue is display instead a
        date
        :param date_str_rep: string represent a date or "overdue"
        """
        self.ids.upcoming_scrollview.add_widget(
            DateButton(text=date_str_rep))
        self.ids.upcoming_scrollview.add_widget(
            DateDividerLabel())

    def completed_task(self, task_id, taskview_ref):
        """
        function will be call if a task checkbox active value change i.e. the
        task completed status change, it will delete the task from upcoming
        task dict and ask the app data handler to add this task to
        completed tasks list. it also remove the task visual from the screen
        :param task_id: task id as int
        :param taskview_ref: address of taskview instance will be remove from
        the screen
        """
        # move task from upcoming to completed by id
        for status in self.upcoming_tasks:

            for date in self.upcoming_tasks[status]:
                date_tasks = self.upcoming_tasks[status][date]

                for i in range(len(date_tasks)):
                    if date_tasks[i]['id'] == task_id:
                        self.app.process_task_handler(
                            'completed',
                            date_tasks[i],
                            date=str(date)
                        )
                        del date_tasks[i]

                        if len(date_tasks) == 0:
                            del self.upcoming_tasks[status][date]

                        break

                else:  # if no break then continue the loop
                    continue

                break  # if inner for loop break then all outer will

            else:
                continue

            break

        # remove task from screen
        self.ids.upcoming_scrollview.remove_widget(taskview_ref)
