from celery import Celery

from elsabuilder.remote.frankenbuild import run, status


app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='file:///tmp/celery/results')


@app.task()
def frankenbuild_run(args):
    output = run(args)
    
    return output


@app.task()
def frankenbuild_status(host):
    output = status(host)

    return output
