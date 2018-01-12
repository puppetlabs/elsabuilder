import json

from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='file:///tmp/celery/results')

@app.task()
def run(args, host=None):
    if not host:
        arch = 'centos-7-x86_64'
        res = floaty.get(arch)
        host = json.loads(res.stdout)[arch]

        with settings(host_string='root@{}'.format(host)):
            install_updates()
            install_tmux()
            install_git()
            install_rbenv()
            install_ruby()
            install_frankenbuilder()


    with settings(host_string='root@{}'.format(host)):
        for d in dirs_to_upload:
            rsync_project(local_dir=d, remote_dir='~/', exclude=['.bundle'])

        run_frankenbuild(' '.join(largs))

