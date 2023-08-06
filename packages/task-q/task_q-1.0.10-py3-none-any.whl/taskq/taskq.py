import os
import pwd
import time
import schedule
from models import Queue
from resources import TaskCreator, TaskHandler, TaskQHelper

def add_task_to_queue(command, context):
    user_id = os.getuid()
    user_name = pwd.getpwuid( os.getuid() ).pw_name

    task = TaskCreator(command, context, user_id, user_name)
    task_id = task.add_to_queue()
    return task_id

def abort_task(task_id):
    response = TaskQHelper.abort_task(task_id)

    if response:
        print('Task with ID={} successfully aborted!'.format(task_id))
    else:
        print('Task with ID={} is not running anymore, impossible to abort!'.format(task_id))

def reset_task(task_id):
    response = TaskQHelper.reset_task(task_id)

    if response:
        print('Task with ID={} successfully reseted!'.format(task_id))
    else:
        print('Task with ID={} is waiting to be processed!'.format(task_id))


def show_task_info(task_id):
    TaskQHelper.task_info(task_id)

def show_queue():
    table = TaskQHelper.show_queue()

    print(table)

def call_task_handler():
    handler = TaskHandler()
    handler.handle()

def start_queue():
    def job():
        print("I'm working...")

    schedule.every(10).minutes.do(job)

    while 1:
        schedule.run_pending()
        time.sleep(1)
