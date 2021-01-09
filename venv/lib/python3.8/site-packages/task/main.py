import click

from task import task_add
from task import task_list
from task import task_rm
from task import task_done
from task import task_describe

__version__ = "0.1.0"


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-v", "--version", is_flag=True, help="print version")
def main(ctx, version) -> int:
    if version:
        print("task version %s" % __version__)
        print("~matteyeux")
    elif ctx.invoked_subcommand is None:
        click.echo(main.get_help(ctx))
    return 0


main.add_command(task_add.main)
main.add_command(task_list.main)
main.add_command(task_rm.main)
main.add_command(task_done.main)
main.add_command(task_describe.main)


if __name__ == '__main__':
    exit(main())
