from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.modalview import ModalView

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from math import ceil


class DateDividerLabel(Label):
    """
    custom label with height 1 to act as divider
    """
    def __init__(self, **kwargs):
        """
        create a label to act as a divider
        """
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(rgba=self.color)
            self.rect = Rectangle()

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        """
        update position and size of rectangle in the canvas instruction. this
        function make sure canvas not take widget default position and size
        """
        self.rect.pos = self.pos
        self.rect.size = self.size


class DateButton(Button):
    """
    custom button use for display date
    """
    def __init__(self, **kwargs):
        """
        create a button to display date title. use button so that the user can
        press the date and that date will be scroll to the top of the viewport
        but this function is not yet implemented
        """
        super().__init__(**kwargs)
        self.text = f'[b][size={int(dp(19))}]' + \
                    ' ' * 4 + f'{self.text}[/size][/b]'

        # before bind / call update on pos & size, they have default value
        #   in python but get auto calculated in kivy
        # bind function pass left side argument to right side function
        self.bind(size=self.update_text_size)

    def update_text_size(self, *args):
        """
        update value of text_size. this function make sure the text_size not
        take widget default/initial size as the value
        """
        self.text_size = self.width, None


class TaskButton(Button):
    """
    custom button use for display task info
    """

    def __init__(self, subject, due_time, overdue=False, **kwargs):
        """
        create a button to display all task info
        :param subject: string format of task description
        :param due_time: time object of task due date
        :param overdue: True if task is overdue, False otherwise
        """
        super().__init__(**kwargs)
        if overdue:
            duetime_color = self.bad_color
            duetime_icon = self.overdue_icon

        else:
            duetime_color = self.good_color
            duetime_icon = self.ontime_icon

        due_time = f'[size=14sp]{duetime_icon}  {due_time}[/size]'
        self.text = f'{subject}\n' + \
                    f'[color={duetime_color}]{due_time}[/color]'

        self.bind(size=self.update_text_size)
        self.bind(texture_size=self.update_height)

    def update_text_size(self, *args):
        """
        update value of text_size. this function make sure the text_size not
        take widget default/initial size as the value
        """
        self.text_size = self.width, None

    def update_height(self, *args):
        """
        update value of widget height. this function make sure the height not
        take widget default/initial texture_size as the value
        """
        if self.texture_size[1] < dp(24):
            self.height = dp(32)
        elif not self.texture_size[1] % dp(8) == 0:
            self.height = dp(8) * ceil(self.texture_size[1] / dp(8)) + dp(12)
        else:
            self.height = self.texture_size[1] + dp(12)


class TaskCheckBox(CheckBox):
    """
    custom checkbox for each task
    """
    def __init__(self, parent, task_id, **kwargs):
        """
        create custom checkbox that allow to change check box color accordingly
        to the app theme
        :param parent: the address of widget that directly contain this widget
        :param task_id: int represent the id of this task
        """
        super().__init__(**kwargs)

        # active return 2 pos arg to lambda -- checkbox address, checkbox value
        self.bind(active=lambda *args: parent.remove_task(task_id))


class TaskView(BoxLayout):
    """
    custom boxlayout to hold TaskCheckBox and TaskButton
    """
    def __init__(self, root, task, due_date=None, overdue=False,
                 checkbox_active=False, **kwargs):
        """
        create custom boxlayout to hold TaskCheckBox and TaskButton and able
        to send it's instance back to the root to remove if task completed
        :param root: address of the screen object
        :param task: dict of task will be use to display
        :param due_date: date object of that task due date (date only)
        :param overdue: True if task is overdue, False otherwise
        :param checkbox_active: True if want checkbox to have it's initial
         state as checked, False otherwise
        """
        super().__init__(**kwargs)
        # self.id = 'task_view_0'
        checkbox = TaskCheckBox(self, task['id'], active=checkbox_active)
        self.add_widget(checkbox)
        self.root = root

        if due_date is None:
            due_time = task['time']
        else:
            due_time = due_date + ' ' + task['time']

        self.add_widget(
            TaskButton(subject=task['subject'], due_time=due_time,
                       overdue=overdue, size_hint=(5, None)))

        self.bind(minimum_height=self.setter('height'))

    def remove_task(self, task_id):
        """
        function will be call when checkbox active (status) change value. call
        this function instead call remove taskview directly to create effect
        the user can see the task be check off (0.3 sec delay) as they check it
        :param task_id: task id as int
        """
        Clock.schedule_once(lambda *args: self.remove_taskview(task_id), 0.3)

    def remove_taskview(self, task_id):
        """
        function to remove that task from the screen
        :param task_id: task id as int
        """
        if self.root.name == 'upcoming_route':
            self.root.completed_task(task_id, taskview_ref=self)
        elif self.root.name == 'completed_route':
            self.root.remove_task(task_id, self)


class ErrorPopup(ModalView):
    """
    custom error popup
    """
    def __init__(self, message, **kwargs):
        """
        create a popup with this message
        :param message: string as message will be display
        """
        super().__init__(**kwargs)
        self.ids.message_label.text = message
