import json
from datetime import datetime

from libs.get_data import add_item_to_dict


def get_curr_date_time():
    """
    get current date time in %Y-%m-%d %H:%M format
    :return: datetime object for current
    """
    curr_time_str = datetime.today().strftime('%Y-%m-%d %H:%M')
    return datetime.strptime(curr_time_str, '%Y-%m-%d %H:%M')


class ProcessTaskHandler:
    def __init__(self, app, _to, task, _date=None):
        """
        :pram app: current app instance
        :pram _to: string represent name of place task will be add to
        :pram task: dict represent task that will get add to other place
        :pram _date: datetime object represent completed time, only need when
        add task to completed tasks list
        """
        self.app = app
        self.upcoming_tasks = app.user_data['upcoming']
        self.completed_tasks = app.user_data['completed']

        self.task = task
        self._date = _date

        if _to == 'upcoming':
            self.add_upcoming_task()
        elif _to == 'completed':
            self.add_completed_task()
        elif _to == 'update_completed':
            self.update_completed_task()
        elif _to == 'save_file':
            self.save_user_data()
        else:
            raise ValueError()

    def add_upcoming_task(self):
        """
        add a task to the upcoming_tasks dict, change apply directly to the
        user_data dict that the whole app read from
        """
        if 'completed_time' in self.task.keys():
            del self.task['completed_time']

        date, time = self.task['time'].split()
        date = datetime.strptime(date, '%Y-%m-%d').date()

        task_due_time = datetime.strptime(self.task['time'], '%Y-%m-%d %H:%M')
        self.task['time'] = time

        if task_due_time <= get_curr_date_time():
            add_item_to_dict(self.upcoming_tasks['overdue'], date, self.task)
        else:
            add_item_to_dict(self.upcoming_tasks['on_time'], date, self.task)

    def add_completed_task(self):
        """
        add a task to the completed_tasks dict, change apply directly to the
        user_data dict that the whole app read from
        """
        self.task['completed_time'] = get_curr_date_time()
        self.task['time'] = self._date + ' ' + self.task['time']

        self.completed_tasks.append(self.task)
        # print('\n' + '-' * 90 + 'to completed: ', self.completed_tasks,
        #       '\n\n')

    def update_completed_task(self):
        """
        loop through the task in completed_tasks and remove all tasks that have
        completed_time more than 24 hours ago
        """
        completed_tasks_len = len(self.completed_tasks)
        curr_time = get_curr_date_time()

        for i in range(completed_tasks_len):
            time_diff = curr_time - self.completed_tasks[i]['completed_time']

            if time_diff.days > 1:
                del self.completed_tasks[i]

    def save_user_data(self):
        """
        reformat current app user_data and write down in a json file
        so the user_data get preserve for future use and diff app instance.
        the written down format is:
            {
            "theme_name": "todolst",
            "largest_id": <current largest id>,
            "upcoming": {
            "overdue": {<overdue tasks>},
            <other upcoming tasks where key is date and
            value is tasks in that date>
            },
            "completed": [<completed tasks>]
            }
        """
        new_data = {
            'theme_name': self.app.user_data['theme_name'],
            'largest_id': self.app.user_data['largest_id'],
            'upcoming': {'overdue': {}}
        }

        for date in self.upcoming_tasks['overdue']:
            new_data['upcoming']['overdue'][date.strftime('%Y-%m-%d')] = \
                self.upcoming_tasks['overdue'][date]

        for date in self.upcoming_tasks['on_time']:
            new_data['upcoming'][date.strftime('%Y-%m-%d')] = \
                self.upcoming_tasks['on_time'][date]

        for task in self.completed_tasks:
            task['completed_time'] = task[
                'completed_time'].strftime('%Y-%m-%d %H:%M')

        new_data['completed'] = self.completed_tasks

        with open('user_data.json', 'w') as outfile:
            json.dump(new_data, outfile)
