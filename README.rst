=================
Elsabuilder
=================



.. image:: https://pyup.io/repos/github/barleyj-puppet/elsabuilder/shield.svg
     :target: https://pyup.io/repos/github/barleyj-puppet/elsabuilder/
     :alt: Updates

Service
--------
Elsabuilder is running as a service in our own cluster and can be accessed through a RESTlike interface. Instead of using arguments on the commandline, you convert those to query parameters for running frankenbuilder. The service does support specifying PR's for testing changes. The request will return the vmpooler host frankenbuilder is running on. Elsabuilder will provide the keyfile and vmpooler arguments for you when used as a service.::

      http://elsabuilder.service.consul.puppet.net:5000/frankenbuild/2016.4.x?install&preserve-hosts=always&pe_manager_pr=5&pe_install_pr=132

      ssgxdr4ry99q1jz.delivery.puppetlabs.net

The request above will run frankenbuilder to build a tarball using the changes in the PR #5 of the puppetlabs-pe_manager repos and PR # 132 in the puppetlabs-pe_install repo, install 2016.4.x and preserve the hosts.

To track the frankenbuilder run, you can query the status endpoint or ssh into the host and attach to the tmux session.

      http://elsabuilder.service.consul.puppet.net:5000/status/ssgxdr4ry99q1jz.delivery.puppetlabs.net

Note that setting up frankenbuilder on the host may take a little while and elsabuilder will not be able to report on the status until then. If you have local changes you want to test, please use the CLI below to test these changes.

CLI
--------
Python utility and that runs frankenbuilder on a vmpooler host. If --host is not specified, it will use vmfloaty to get a 'centos-7-x86_64' image, install all libraries needed for frankenbuilder and run frankenbuild with any arguments specified on the command line. If any Frankenbuilder arguments have values that are directories on your localhost, it will rsync those directories to the remote host in the root home directory and update the paths specified to frankenbuilder.


Installation
--------
* Clone the repo.::

      git clone git@github.com:barleyj-puppet/elsabuilder.git

* Place any keys you need to clone Puppet repos or run frankenbuilder in your $HOME/.ssh directory

* Install elsabuilder. From within the elsabuilder directory run.::

      sudo pip install .

      # If you are doing development, this will symlink the source directory
      sudo pip install --editable .


Features
--------
* Run a frankenbuild on a vmpooler instance.::

      elsabuilder frankenbuild 2017.3.x --upgrade-from=2017.2.x --install --upgrade --smoke --ha --vmpooler --keyfile=~/.ssh/id_rsa-acceptance --preserve-hosts=always --pe_manager=../../puppetlabs-pe_manager --pe_install=../../puppetlabs-pe_install

      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: [root@ssgxdr4ry99q1jz frankenbuilder]# ./frankenbuilder 2017.3.x --upgrade-from=2017.2.x --install --upgrade --smoke --ha --vmpooler --keyfile=~/.ssh/id_rsa-acceptance --preserve-hosts=always --pe_manager=../puppetlabs-pe_manager --pe_install=../puppetlabs-pe_install
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Cleaning /tmp/frankenmodules...
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Done.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Removing cached agent artifacts...
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Cloning git@github.com:puppetlabs/pe_acceptance_tests.git...
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Cloning into '/tmp/frankenmodules/pe_acceptance_tests'...
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: remote: Counting objects: 19798, done.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: remote: Compressing objects: 100% (95/95), done.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: remote: Total 19798 (delta 83), reused 67 (delta 39), pack-reused 19664
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Receiving objects: 100% (19798/19798), 6.16 MiB | 0 bytes/s, done.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Resolving deltas: 100% (12024/12024), done.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: remote: Counting objects: 3101, done.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: remote: Compressing objects: 100% (5/5), done.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: remote: Total 3101 (delta 917), reused 917 (delta 917), pack-reused 2179
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Receiving objects: 100% (3101/3101), 548.22 KiB | 0 bytes/s, done.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: Resolving deltas: 100% (1750/1750), completed with 523 local objects.
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out: From github.com:puppetlabs/pe_acceptance_tests
      [root@ssgxdr4ry99q1jz.delivery.puppetlabs.net] out:  * [new ref]         refs/pull/1/head -> puppetlabs/pr/1

* Get the frankenbuilder status.::

      elsabuilder frankenbuilder_status --host ssgxdr4ry99q1jz.delivery.puppetlabs.net

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
