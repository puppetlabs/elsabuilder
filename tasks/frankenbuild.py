import os

from celery import Celery

from elsabuilder.remote.frankenbuild import install, run, status


app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='couchdb://couchdb:5984')


@app.task()
def get_version():
    return {
        "worker_image_id": os.environ["HOSTNAME"],
        "worker_version": open("version").read().strip(),
        }


@app.task()
def frankenbuild_install(host=None):
    output = install(host)

    return output


@app.task()
def frankenbuild_run(host, args):
    output = run(args, host=host)
    
    return output


@app.task()
def frankenbuild_status(host):
    output = status(host)

    return output
