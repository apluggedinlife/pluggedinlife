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
env.gunicorn_pid_root = '/var/run/gunicorn_pluggedinlife.pid'

# local
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
EXCLUDES = ['bin', '_old', 'include', 'lib', '*.psd', '*.ai', '.Python', 'Fonts', 'build']

def start():
    with cd(env.root):
        sudo(env.activate + ' && gunicorn -b 127.0.0.1:5000 --pid=%s server:app' % env.gunicorn_pid_root)

def reload():
    with cd(env.root):
        sudo('[ -f %(gunicorn_pid_root)s ] && kill -HUP $(cat %(gunicorn_pid_root)s)' % {
            'gunicorn_pid_root': env.gunicorn_pid_root
        })

def stop():
    with cd(env.root):
        sudo('[ -f %(gunicorn_pid_root)s ] && kill $(cat %(gunicorn_pid_root)s)' % {
            'gunicorn_pid_root': env.gunicorn_pid_root
        })

def publish():
    project.rsync_project(
        remote_dir=env.root,
        exclude=EXCLUDES,
        local_dir=ROOT_PATH + '/',
    )

def deploy():
    publish()
    with cd(env.root):
        run('virtualenv .')
        run(env.activate + ' && pip install -r requirements.txt')
