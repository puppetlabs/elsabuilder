import json
import os
import sys

import click

from log import Logger, logger_group, DEBUG
from remote.frankenbuild import run, status

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

    run(largs, dirs_to_upload, host)


@cli.command()
@click.option('--host', default=None)
def frankenbuild_status(host):
    output = status(host)
    click.echo(output)

if __name__ == '__main__':
    cli()
