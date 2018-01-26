from flask import Flask, request

from elsabuilder.remote.frankenbuild import get_host
from tasks.frankenbuild import frankenbuild_install, frankenbuild_run, frankenbuild_status


app = Flask(__name__)


@app.route("/install")
def install():
    host = get_host()
    frankenbuild_install.delay(host)
    
    return host


# /frankenbuild/2017.3.x?upgrade-from=2017.2.x&install&upgrade&smoke&ha&vmpooler&keyfile=~/.ssh/id_rsa-acceptance&preserve-hosts=always&pe_install_pr=233&puppet_enterprise_pr=1398
@app.route("/frankenbuild/<version>")
def run(version, host=None):
    args = request.args

    largs = [version]
    for k,v in args.items():
        if v:
            largs.append('--{}={}'.format(k,v))
        else:
            largs.append('--{}'.format(k))

    host = get_host()
    frankenbuild_install.apply_async(kwargs={'host': host}, link=frankenbuild_run.s(largs))
    
    return host


@app.route("/status/<host>")
def status(host):
    job = frankenbuild_status.delay(host)
    output = job.get()
    
    return output.replace('\n', '<br>')
