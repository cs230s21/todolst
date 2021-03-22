import json
import datetime


# date_format = '%Y-%m-%d'
# data_time_format = '%Y-%m-%d %H:%M'

def _hex_to_rgb(hex_color):
    """
    :param hex_color: valid hex code of a color
    :return: rgba value each between 0 and 1
    """
    hex_color = hex_color.lstrip('#')
    hex_color = list(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    result = []
    for value in hex_color:
        result.append(round(value / 255, 3))

    result.append(1.0)

    return result


def get_theme_palette(theme_name):
    """
    get color data of the theme_name
    :param theme_name: name of the theme - todolst, dark, neutral
    :return: color palette for the theme
    """
    if theme_name not in ['todolst', 'dark', 'neutral']:
        raise ValueError

    try:
        with open('assets/theme_palettes.json', 'r') as f:
            themes_data = json.load(f)

        theme_data = themes_data[theme_name]
        theme_palette = {}

        for color in theme_data:
            if color == "good_color" or color == "bad_color":
                theme_palette[color] = theme_data[color]
            else:
                theme_palette[color] = _hex_to_rgb(theme_data[color])

        # print(theme_palette)
        return theme_palette

    except Exception as e:
        print(e)


def add_item_to_dict(dict_obj, key, value):
    """
    add an item to a list inside a dict or create a list contain this item in
    the dict with it's associate date key in dict
    -> in dict_obj -- key: [value]
    :param dict_obj: dictionary will hold this list
    :param key: key for the list
    :param value: value of the item
    :return: add list of item to the dict
    """
    if key not in dict_obj.keys():
        if type(value) == list:
            dict_obj[key] = value
        else:
            dict_obj[key] = [value]

    elif type(dict_obj[key]) == list:
        if type(value) == list:
            for item in value:
                dict_obj[key].append(item)
        else:
            dict_obj[key].append(value)


def get_upcoming_tasks(upcoming_data):
    """
    extract upcoming tasks in upcoming_data and format to dict object where key
    is due date and value is list of tasks on that day then put those task dict
    in to 2 categories overdue and on_time
    :return: dict of overdue and on_time dict of upcoming tasks
    """

    upcoming_tasks = {'overdue': {}, 'on_time': {}}
    curr_date = datetime.date.today()

    for date in upcoming_data:
        # put all existed overdue tasks to new overdue
        if date == 'overdue':
            for overdue_date in upcoming_data['overdue']:
                overdue_date_obj = datetime.datetime. \
                    strptime(overdue_date, "%Y-%m-%d").date()
                upcoming_tasks['overdue'][overdue_date_obj] = \
                    upcoming_data['overdue'][overdue_date]

        # check if task can go to overdue or on_time
        else:
            due_date_obj = datetime.datetime. \
                strptime(date, "%Y-%m-%d").date()

            # all tasks with date prior than today will go in overdue
            if due_date_obj < curr_date:
                add_item_to_dict(upcoming_tasks['overdue'], due_date_obj,
                                 upcoming_data[date])

            # if task with today date then check time
            elif due_date_obj == curr_date:
                curr_time = datetime.datetime.now().time()

                # all tasks with pasted time will go in overdue
                for task in upcoming_data[date]:
                    task_due_time = datetime.datetime.strptime(
                        task['time'], '%H:%M').time()

                    if task_due_time > curr_time:
                        add_item_to_dict(upcoming_tasks['on_time'],
                                         curr_date, task)
                    else:
                        add_item_to_dict(upcoming_tasks['overdue'],
                                         curr_date, task)

            # all task that not filter in overdue can go in on_time
            else:
                upcoming_tasks['on_time'][due_date_obj] = \
                    upcoming_data[date]

    # print(upcoming_tasks)
    return upcoming_tasks


def get_next7dates():
    """
    get date for the next 7 days
    :return: list of 7 datetime object represent next 7 days
    """
    return [datetime.date.today() + datetime.timedelta(days=i) for i in
            range(8)]


def get_completed_tasks(completed_data):
    """
    get completed task within 24h from completed_data and format all
    completed_time to datetime object
    :return: list of completed tasks within 24 hours
    """

    completed_tasks = []
    curr_datetime = datetime.datetime.now()
    period_24h = datetime.timedelta(days=1)

    for task in completed_data:
        completed_time_obj = datetime.datetime.strptime(
            task['completed_time'], '%Y-%m-%d %H:%M')

        if (curr_datetime - completed_time_obj) < period_24h:
            task['completed_time'] = completed_time_obj
            completed_tasks.append(task)

    # print(completed_tasks)
    return completed_tasks


def get_user_data():
    """
    step app need to run every time the app open - get all user_data and
    reformat
    :return: dict of all app data formatted
    """
    try:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)

        app_data = {
            'theme_name': user_data['theme_name'],
            'largest_id': user_data['largest_id'],
            'upcoming': get_upcoming_tasks(user_data['upcoming']),
            'completed': get_completed_tasks(user_data['completed'])
        }

        # print(app_data)
        return app_data

    except Exception as e:
        print(e)
