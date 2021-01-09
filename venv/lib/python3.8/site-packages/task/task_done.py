import click
from click_default_group import DefaultGroup

from task import utils


@click.group(
    name='done',
    cls=DefaultGroup,
    default='task-done',
    default_if_no_args=True
)
def main():
    """Finished task."""


@main.command()
@click.argument('task_id', type=click.INT)
def task_done(task_id: int = 0) -> int:
    """Task is done."""
    if utils.does_db_exist()[0] is False:
        # TODO better prints than this
        print("Database not found")
        print("See doc")
        return 1

    # 0 should be the latest task that can be set to done
    new_done = utils.set_task_done(task_id)
    utils.update_task(task_id)
    print(f"Done {new_done}")
