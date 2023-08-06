import time
import click
import schedule
from subprocess import Popen


def job():
    # click.echo('Calling Task Handler')
    proc = Popen('taskq call-task-handler', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    proc.wait()

    return proc.pid

def bot():
    schedule.every(10).seconds.do(job)

    while 1:
        # click.echo('Running...')
        schedule.run_pending()
        # click.echo('...')
        time.sleep(1)
        # click.echo('Done!\n')


bot()
