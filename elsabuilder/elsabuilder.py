import json
import os
import sys

import click
from log import Logger, logger_group, DEBUG
from fabric.context_managers import settings
from fabfile import *
from fabric.contrib.project import rsync_project
from sh import floaty

#StreamHandler(sys.stdout).push_application()
log = Logger(__name__)
logger_group.add_logger(log)


@click.group()
@click.option('--debug', is_flag=True)
def cli(debug):
    if debug:
        logger_group.level = DEBUG


@cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('--host', default=None)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def frankenbuild(host, args):
    largs = list(args)
    dirs_to_upload = []
    
    for i,arg in enumerate(largs):
        if '=' in arg:
            k,v = arg.split('=')
            if os.path.isdir(v):
                remote_dir = os.path.join('..', os.path.basename(v))
                largs[i] = '='.join([k, remote_dir])
                dirs_to_upload.append(v)

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


@cli.command()
@click.option('--host', default=None)
def frankenbuild_status(host):
    with settings(host_string='root@{}'.format(host)):
        tmux_status()


if __name__ == '__main__':
    cli()
