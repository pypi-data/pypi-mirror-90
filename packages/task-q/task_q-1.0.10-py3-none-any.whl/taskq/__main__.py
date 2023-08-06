import os
import sys
import pwd
import click
import peewee
from subprocess import Popen

# from models import Queue
# from resources import TaskCreator, TaskHandler, TaskQHelper


TH_BOT_PID = None


@click.group()
@click.version_option(version='1.0.10')
def main():
    """TaskQ - Task queue tool CLI"""
    pass


@main.command()
@click.argument('home_path', required=True)
def install(home_path):
    from taskq.utils import Configuration
    config = Configuration()
    config.install(home_path)
    initdb()
    ENV = config.loadEnv()
    fix_db_permissions(ENV['db_path'])


@main.command()
@click.argument('command', required=True)
@click.argument('context', required=False)
def add_task_to_queue(command, context):
    from taskq.resources import TaskCreator
    user_id = os.getuid()
    user_name = pwd.getpwuid( os.getuid() ).pw_name

    task = TaskCreator(command, context, user_id, user_name)
    task_id = task.add_to_queue()
    return task_id


@main.command()
@click.argument('task_id', required=True)
def abort_task(task_id):
    from taskq.resources import TaskQHelper
    response = TaskQHelper.abort_task(task_id)

    if response:
        click.echo('Task with ID={} successfully aborted!'.format(task_id))
    else:
        click.echo('Task with ID={} is not running anymore, impossible to abort!'.format(task_id))


@main.command()
@click.argument('task_id', required=True)
def reset_task(task_id):
    from taskq.resources import TaskQHelper
    response = TaskQHelper.reset_task(task_id)

    if response:
        click.echo('Task with ID={} successfully reseted!'.format(task_id))
    else:
        click.echo('Task with ID={} is waiting to be processed!'.format(task_id))


@main.command()
@click.argument('task_id', required=True)
def show_task_info(task_id):
    from taskq.resources import TaskQHelper
    table = TaskQHelper.task_info(task_id)

    click.echo(table)

@main.command()
@click.argument('mode', required=False)
def show_queue(mode):
    from taskq.resources import TaskQHelper
    table = TaskQHelper.show_queue(mode)

    click.echo(table)


@main.command()
def call_task_handler():
    from taskq.resources import TaskHandler
    handler = TaskHandler()
    message = handler.handle()

    # click.echo(message)

def initdb():
    from taskq.models import Queue
    # try:
    Queue.create_table()
    click.echo("Table 'Queue' created successfully!")
    # except peewee.OperationalError:
    #     click.echo("Table 'Queue' already exists!")

def fix_db_permissions(db_path):
    with Popen(['sudo chmod g+w {}'.format(db_path)], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True) as proc:
        proc.wait()

@main.command()
def start():
    import taskq
    task_handler = os.path.join(taskq.__path__[0], 'task-handler.py')
    proc = Popen('python {}'.format(task_handler), shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    click.echo("Task Handler Bot PID: {}".format(proc.pid))


@main.command()
def stop():
    import taskq

    print(TH_BOT_PID)

















if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("TaskQ")
    main()
