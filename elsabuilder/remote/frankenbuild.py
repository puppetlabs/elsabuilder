import json

from fabric.context_managers import settings
from fabfile import *
from fabric.contrib.project import rsync_project
from sh import floaty


def get_host():
    arch = 'centos-7-x86_64'
    res = floaty.get(arch, '--json', _timeout=5)
    host = json.loads(res.stdout)[arch][0]

    return host


def install(host=None):
    if not host:
        host = get_host()

    with hide('output'), settings(host_string='root@{}'.format(host)):
        install_updates()
        install_tmux()
        install_git()
        install_rbenv()
        install_ruby()
        install_frankenbuilder()

    return host


def run(args, upload_dirs=[], host=None):
    if not host:
        host = get_host()
        install(host)

    with hide('output'), settings(host_string='root@{}'.format(host)):
        for d in upload_dirs:
            rsync_project(local_dir=d, remote_dir='~/', exclude=['.bundle'])

        run_frankenbuild(' '.join(args))

    return host


def status(host):
    with hide('output', 'running'), settings(host_string='root@{}'.format(host)):
        return tmux_status()
