import json
import os

from celery.result import AsyncResult
from flask import Flask, request

from elsabuilder.remote.frankenbuild import get_host
from tasks.frankenbuild import frankenbuild_install, frankenbuild_run, frankenbuild_status, get_version


app = Flask(__name__)
default_params = {'vmpooler': None,
                  'keyfile': '~/.ssh/id_rsa-acceptance',
                  }

@app.route("/version")
def version():
    worker_version = get_version()
    return json.dumps({
        "web_image_id": os.environ["HOSTNAME"],
        "web_version": open("version").read().strip(),
        "worker_image_id": worker_version['worker_image_id'],
        "worker_version": worker_version['worker_version'],
        })


@app.route("/install")
def install():
    host = get_host()
    frankenbuild_install.delay(host)
    
    return host


# /frankenbuild/2017.3.x?upgrade-from=2017.2.x&install&upgrade&smoke&ha&vmpooler&keyfile=~/.ssh/id_rsa-acceptance&preserve-hosts=always&pe_install_pr=233&puppet_enterprise_pr=1398
@app.route("/frankenbuild/<version>")
def run(version, host=None):
    args = default_params.copy()
    args.update({str(k): str(v) for k,v in request.args.items()})

    largs = [version]
    for k,v in args.items():
        if v:
            largs.append('--{}={}'.format(k,v))
        else:
            largs.append('--{}'.format(k))

    host = get_host()
    task = frankenbuild_install.apply_async(task_id=host, kwargs={'host': host}, link=frankenbuild_run.s(largs))
    
    return host


@app.route("/status/<host>")
def status(host):
    res = AsyncResult(host)
    if res.ready():
        job = frankenbuild_status.delay(host)
        output = job.get()
    else:
        output = 'Setting up host: {}'.format(host)

    return output.replace('\n', '<br>')
