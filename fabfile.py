#fab -f fabfile.py <command>

from __future__ import with_statement

import os
from fabric.api import *
from fabric.contrib import project

# I have entries in /etc/hosts which make these names work. 
# If I didn't, I'd just use IP addresses.
env.hosts = ['kaltorak']
env.user = 'webadmin'
env.project_name = 'pluggedinlife'

#paths
env.root = "/var/www/%s" % env.project_name
env.bin_root = os.path.join(env.root, 'bin')
env.activate = 'source %s' % os.path.join(env.bin_root, 'activate')
env.service_root = '/var/sv/%s' % env.project_name

# local
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
EXCLUDES = ['bin', '_old', 'include', 'lib', '*.psd', '*.ai', '.Python', 'Fonts', 'build']

def publish():
    project.rsync_project(
        remote_dir=env.root,
        exclude=EXCLUDES,
        local_dir=ROOT_PATH + '/',
    )

def prepare_service():
    sudo('mkdir -p %s' % env.service_root)
    sudo('ln -s %s %s' % (os.path.join(env.root, 'run'), os.path.join(env.service_root, 'run')))
    sudo('chmod +x %s' % os.path.join(env.service_root, 'run'))
    sudo('ln -s %s /etc/service/%s' % (env.service_root, env.project_name))

def deploy():
    publish()
    with cd(env.root):
        run('virtualenv .')
        run(env.activate + ' && pip install -r requirements.txt')
        prepare_service()
