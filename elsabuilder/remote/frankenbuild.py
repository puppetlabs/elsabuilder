import json

from fabric.context_managers import settings
from fabfile import *
from fabric.contrib.project import rsync_project
from sh import floaty


def run(args, upload_dirs=[], host=None):
    if not host:
        arch = 'centos-7-x86_64'
        res = floaty.get(arch)
        host = json.loads(res.stdout)[arch]

        with hide('output'), settings(host_string='root@{}'.format(host)):
            install_updates()
            install_tmux()
            install_git()
            install_rbenv()
            install_ruby()
            install_frankenbuilder()


    with hide('output'), settings(host_string='root@{}'.format(host)):
        for d in upload_dirs:
            rsync_project(local_dir=d, remote_dir='~/', exclude=['.bundle'])

        run_frankenbuild(' '.join(args))

    return host


def status(host):
    with hide('output', 'running'), settings(host_string='root@{}'.format(host)):
        return tmux_status()
