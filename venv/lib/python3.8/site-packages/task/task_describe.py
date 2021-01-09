import click
from click_default_group import DefaultGroup

from task import utils


@click.group(
    name='describe',
    cls=DefaultGroup,
    default='describe-task',
    default_if_no_args=True
)
def main():
    """Describe task."""


@main.command()
@click.argument('task_id', type=click.INT, required=False)
def describe_task(task_id: int = None) -> int:
    """Describe task."""
    if utils.does_db_exist()[0] is False:
        print("[e] no database found. Please add task first")
        return 0
    try:
        task = utils.get_one_task(task_id)[0]
    except TypeError:
        print(f"No task found with ID {task_id}")
        return 0
    print("\x1b[4mname\x1b[0m         | \x1b[4mvalue\x1b[0m")
    print("-------------------------------")
    print(f"ID           | {task[0]}")
    print(f"Project      | {task[1]}")
    print(f"Task         | {task[2]}")
    print(f"Status       | {'done' if task[5] == 1 else 'todo'}")
    print(f"Urgency      | {task[3]}")
    print(f"Due          | {task[4]}")
    print(f"Created at   | {task[6]}")
    print(f"Last updated | {task[7]}")
    return 0
