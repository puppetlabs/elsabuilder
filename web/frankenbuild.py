import json

from celery.result import AsyncResult
from flask import Flask, request

import elsabuilder
from elsabuilder.remote.frankenbuild import get_host
from tasks.frankenbuild import frankenbuild_install, frankenbuild_run, frankenbuild_status, get_version


app = Flask(__name__)
default_params = {'vmpooler': None,
                  'keyfile': '~/.ssh/id_rsa-acceptance',
                  }

@app.route("/version")
def version():
    worker_version = get_version.delay().get()
    return json.dumps({
        "web": elsabuilder.version_info,
        "worker": worker_version,
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
    if res.failed():
        status = {
            'status': 'failed',
            'message': res.result.message,
            }
        if 'debug' in request.args:
            status['output'] = res.traceback
        output = json.dumps(status)
    elif res.ready():
        job = frankenbuild_status.delay(host)
        output = job.get()
    else:
        output = json.dumps({
            'status': 'installing',
            'message': 'Setting up host: {}'.format(host),
            })

    return output.replace('\n', '<br>')
