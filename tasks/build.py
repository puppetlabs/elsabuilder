from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='file:///tmp/celery/results')

@app.task()
def add_together(a, b):
    return a + b
