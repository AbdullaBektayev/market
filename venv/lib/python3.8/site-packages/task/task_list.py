import click
import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
from click_default_group import DefaultGroup

from task import utils


@click.group(
    name='ls',
    cls=DefaultGroup,
    default='list-tasks',
    default_if_no_args=True

)
def main():
    """List tasks."""


def get_date_age(task_date: str, is_due: bool = False) -> str:
    """Get age of date."""
    if is_due:
        if task_date is None or task_date == "":
            return ""
        else:
            task_date = f"{task_date} 00:00:00"

    task_date = datetime.datetime.strptime(task_date, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    if is_due:
        age = relativedelta(task_date, now)
    else:
        age = relativedelta(now, task_date)

    if age.years != 0:
        age = age.years
        age_type = "year"
    elif age.months != 0:
        age = age.months
        age_type = "month"
    elif age.days != 0:
        age = age.days
        age_type = "day"
    elif age.hours != 0:
        age = age.hours
        age_type = "hour"
    elif age.minutes != 0:
        age = age.minutes
        age_type = "minute"
    else:
        age = age.seconds
        age_type = "second"
    return f"{age} {age_type + 's' if age > 1 else age_type}"


def prettify_header(header) -> tuple:
    """Pretty header."""
    new_header = list()
    for data in header:
        new_header.append(f"\x1b[4m{data}\x1b[0m")
    return new_header


def prettify_tasks(tasks: list) -> list:
    """Set black background
    and red tasks when needed.
    """
    cnt = 0
    new_tasks = list()
    for task in tasks:
        row_cnt = 0
        new_task = list()
        for row in task:
            if (cnt % 2) != 0:
                new_task.append(f'\x1b[40m{row}')
            else:
                new_task.append(f'{row}')
            if row_cnt == 4:
                due = row
            row_cnt += 1
        age = get_date_age(row)
        due_age = get_date_age(due, True)
        new_task[-1] = f"{age}\x1b[0m"
        new_task[4] = due_age
        cnt += 1
        new_tasks.append(new_task)
    return new_tasks


@main.command()
@click.argument('what', type=click.STRING, required=False)
def list_tasks(what: str = None) -> int:
    """List tasks. You specify 'all' or 'done'"""
    if utils.does_db_exist()[0] is False:
        utils.create_db()
        return 1

    header = ("ID", "Project", "Task", "Urgency", "Due", "Age")
    header = prettify_header(header)
    tasks = utils.list_tasks(what)

    pretty_tasks = prettify_tasks(tasks)
    print(tabulate(pretty_tasks, headers=header, tablefmt="plain"))
