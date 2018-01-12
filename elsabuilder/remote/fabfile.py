from os.path import isdir

from fabric.api import *
from fabric.contrib import files

# floaty get centos-7-x86_64
env.user = 'root'
env.key_filename = '/Users/jayson.barley/.ssh/id_rsa-acceptance'

# _run = run

# def run(cmd):
#     pass

@task
def run_ha_tests(config='my.cfg', pe_version='2017.3.0', upgrade_from='2017.2', upgrade_to='2017.3'):
    put(local_path=config, remote_path='pe_acceptance_tests/acceptance/high_availability')
    if isdir(upgrade_from):
        put(local_path=upgrade_from, remote_path='pe_acceptance_tests/acceptance/high_availability')
    if isdir(upgrade_to):
        put(local_path=upgrade_to, remote_path='pe_acceptance_tests/acceptance/high_availability')
    with cd('pe_acceptance_tests/acceptance/high_availability'), shell_env(RBENV_VERSION='2.4.2'):
        run('bundle install --path .bundle')
        run('bundle exec rake upgrade_acceptance pe_family={} pe_version={} UPGRADE_FROM={} PRESERVE_HOSTS=always BEAKER_HOSTS={} BEAKER_TESTS=../../setup/high_availability/upgrade.rb'.format(upgrade_to, pe_version, upgrade_from, config))
#        run('bundle exec rake pe_acceptance pe_family=2017.2 pe_version=2017.2.0 PRESERVE_HOSTS=always BEAKER_HOSTS=my.cfg BEAKER_TESTS=../../setup/high_availability/install.rb')


@task
def run_frankenbuild(args):
    with cd('frankenbuilder'):
        with settings(warn_only=True):
            run('tmux set-option history-limit 999999')
            run('tmux new-session -d -s frankenbuild')

        run("tmux send-keys './frankenbuilder {}'".format(args))
        run('tmux send-keys ENTER')
        
@task
def install_acceptance_tests():
    run('gem install beaker')
    put('~/.ssh', '~/', mirror_local_mode=True)
    run('git clone git@github.com:puppetlabs/pe_acceptance_tests.git')


@task
def install_frankenbuilder():
    put('~/.ssh', '~/', mirror_local_mode=True)
    run('git clone git@github.com:puppetlabs/frankenbuilder.git')


@task
def install_rbenv():
    run('git clone https://github.com/rbenv/rbenv.git ~/.rbenv')
    run('echo \'export PATH="$HOME/.rbenv/bin:$PATH"\' >> ~/.bash_profile')
    run('echo \'eval "$(rbenv init -)"\' >> ~/.bash_profile')
    run('source ~/.bash_profile')
    run('mkdir -p "$(rbenv root)"/plugins')
    run('git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build')


@task
def install_ruby(version='2.4.2'):
    run('rbenv install -s {}'.format(version))
    run('rbenv global {}'.format(version))
        
    run('gem install bundle')


@task
def install_git():
    run('yes | yum install git')


@task
def install_updates():
    run('yum install -y git-core zlib zlib-devel gcc-c++ patch readline readline-devel libyaml-devel libffi-devel openssl-devel make bzip2 autoconf automake libtool bison curl sqlite-devel')


@task
def install_tmux():
    run('yes | yum install tmux')


@task
def latest_sut():
    run('cat ./pe_acceptance_tests/acceptance/high_availability/log/latest/sut.log')


@task
def connect_db(database):
    open_shell('sudo -u pe-postgres /opt/puppetlabs/server/bin/psql {}'.format(database))


@task
def tmux_status():
    output = run('tmux capture-pane -pt "$frankenbuild:0" -S -999999')

    return output.stdout
