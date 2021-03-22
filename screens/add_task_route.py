import datetime
from dateutil import parser

from kivy.uix.screenmanager import Screen
from libs.custom_kv_widget import ErrorPopup


# Custom Exception used to catch errors in add_task_to_upcoming().
class AddTaskError(Exception):
    def __init__(self, message):
        """
        function extract and create error message to be display
        :param message: error message as string or error object
        """
        if type(message) is str:
            self.message = str(message)
        else:
            self.message = 'Invalid deadline'


def _create_due_time(datetime_rep):
    """
    - turns the user-inputted datetime into a valid string represent due
    datetime
    - the function raise AddTaskError if datetime object represent due
    time cannot be create or when the due date time is smaller than current
    time i.e. already past.
    - the function has some input validation but also allow the user to have
    wide range of input format i.e. all common known date time format along
    with some abbreviation.
    eg: 'tdy', '2day', '2de', '2da', '2d', 'today' for today
    eg2: 'tomw', 'tmw', 'tmr', '2moro', 'tomorrow' for tomorrow
    - the function add the time 23:59 as due time if the user only specified
    due date
    - the function assume due date is current date i.e. today if the user only
    provide due time
    :pram datetime_rep: string representation of a datetime
    :return: string represent datetime in form Year-month-date Hour:Minute
    """
    if not datetime_rep:
        return str(datetime.date.today()) + " 23:59"

    datetime_rep = datetime_rep.lower()
    datetime_lst = datetime_rep.split()

    if len(datetime_lst) < 3 and ':' not in datetime_rep:
        datetime_lst.append('23:59')
    elif len(datetime_lst) == 1 and ':' in datetime_rep:
        datetime_lst.insert(0, 'tdy')

    for i in range(len(datetime_lst)):

        if datetime_lst[i] in ['tdy', '2day', '2de', '2da', '2d', 'today']:
            datetime_lst[i] = str(datetime.date.today())
            break

        elif datetime_lst[i] in ['tomw', 'tmw', 'tmr', '2moro', 'tomorrow']:
            datetime_lst[i] = str(
                datetime.date.today() + datetime.timedelta(days=1))
            break

    datetime_rep = ' '.join(datetime_lst)

    try:
        datetime_rep = parser.parse(datetime_rep)
    except ValueError or OverflowError as e:
        raise AddTaskError(e)

    if datetime_rep < datetime.datetime.today():
        raise AddTaskError("Due time can't smaller than current time")
    else:
        return datetime_rep.strftime('%Y-%m-%d %H:%M')


class AddTaskRoute(Screen):
    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        """
        super().__init__(**kwargs)
        self.app = app

    def add_task_to_upcoming(self, button_instance):
        """
        turns the task information the user inputs into a dictionary that can
        be transferred back and displayed on UpcomingRoute. function raise
        open popup if the task description missing or AddTaskError raised due
        to unable to create datetime object represent due time
        :param button_instance: button object indicate which button is being
        press
        :return: The task in dictionary form, task_as_dict
        """
        try:
            if not self.ids.subject.text and self.ids.time.text:
                error = 'Missing task description'
                raise AddTaskError(error)
            elif not self.ids.subject.text and not self.ids.time.text:
                self.go_to_upcoming(button_instance)
                return

            self.app.user_data["largest_id"] += 1

            new_task = {
                "id": self.app.user_data["largest_id"],
                "subject": self.ids.subject.text,
                "time": _create_due_time(self.ids.time.text),
                "priority": "none"
            }

            self.ids.subject.text = ''
            self.ids.time.text = ''

            self.app.process_task_handler('upcoming', new_task)
            self.go_to_upcoming(button_instance)

        except AddTaskError as error:
            ErrorPopup(error.message).open()

    def go_to_upcoming(self, button_instance):
        """
        function call to transition from AddTaskRoute back to UpcomingRoute.
        function will not allow transition to take place if a popup show up or
        when the button is adding and stay not adding and leave
        :param button_instance: button object to check which button (add button
        or paper plane button) being press
        """
        if button_instance is self.ids.add_leave_btn:
            self.app.route_manager.current = "upcoming_route"
            self.app.route_manager.transition.direction = "down"
