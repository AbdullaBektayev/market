import click
from click_default_group import DefaultGroup

from task import utils


@click.group(
    name='rm',
    cls=DefaultGroup,
    default='remove-task',
    default_if_no_args=True
)
def main():
    """Remove a task."""


@main.command()
@click.argument('task_id', type=click.INT)
def remove_task(task_id: int = 0) -> int:
    """Remove a task."""
    if utils.does_db_exist()[0] is False:
        print("Database not found")
        return 1

    # if task is 0 make sure we remove latest task entry
    utils.remove_entry(task_id)
    print(f"Removed task {task_id}")
    return task_id
