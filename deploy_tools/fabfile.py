from fabric import task
from fabric import Connection
import os
import random

REPO_URL = 'https://github.com/kevinlee584/myPythonDemo.git'

@task
def deploy(ctx):
    site_folder = '/home/%s/sites/%s' % (os.environ['user'], os.environ['host'])
    source_folder = site_folder + '/source'
    _creae_directory_structure_if_necessary(ctx, site_folder)
    _get_latest_source(ctx, source_folder)
    _update_settings(ctx, source_folder, os.environ['ip'])
    _update_venv(ctx, source_folder)
    _update_static_files(ctx, source_folder)
    _update_database(ctx, source_folder)

def _creae_directory_structure_if_necessary(ctx, site_folder):
    for subfolder in ('database', 'static', 'venv', 'source'):
        ctx.run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(ctx, source_folder):

    if ctx.run('test -d %s/.git' % (source_folder, ), warn=True).ok:
        ctx.run('cd %s && git fetch' % (source_folder,))
    else:
        ctx.run('git clone %s %s && cd %s' % (REPO_URL, source_folder, source_folder))
    
    current_commit = ctx.run('cd %s && git log -n 1 --format=%%H' % (source_folder,)).stdout
    ctx.run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(ctx: Connection, source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    ctx.run('sed \'s/DEBUG = True/DEBUG = False/g\' %s > /dev/null' % settings_path)
    ctx.run('sed \'s/ALLOWED_HOSTS =.+$/ALLOWED_HOSTS = ["%s"]/g\' %s > /dev/null' % (site_name, settings_path))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not ctx.run('test -f %s' % (secret_key_file,), warn=True).ok:
        chars = "12345678910"
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        ctx.run('echo SECRET_KEY = %s >> %s' % (key, secret_key_file))
    ctx.run('echo \'\nfrom .secret_key import  SECRET_KEY\' >> %s' % (settings_path, ))

def _update_venv(ctx: Connection, source_folder):
    venv_folder = source_folder + '/../venv'
    if not ctx.run('test -f %s/bin/pip' % (venv_folder,), warn=True).ok:
        ctx.run('python3 -m venv %s' % (venv_folder))
    ctx.run('%s/bin/pip install -r %s/requirements.txt' % (venv_folder, source_folder))

def _update_static_files(ctx: Connection, source_folder):
    ctx.run('cd %s  && ../venv/bin/python3 manage.py collectstatic --noinput' % (source_folder,))

def _update_database(ctx: Connection, source_folder):
    ctx.run('cd %s && ../venv/bin/python3 manage.py makemigrations lists' % (source_folder, ))
    ctx.run('cd %s && ../venv/bin/python3 manage.py migrate' % (source_folder, ))
