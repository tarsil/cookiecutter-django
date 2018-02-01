
import os
import sys

from jinja2 import Environment, FileSystemLoader
from invoke import run, task


def _template_file(template, destination, template_dir='/var/www/deploy/'):
    environment = Environment(loader=FileSystemLoader(template_dir))
    template = environment.get_template(template)
    rendered_template = template.render(os.environ)
    if os.path.isfile(destination):
        os.unlink(destination)
    with open(destination, 'w') as f:
        f.write(rendered_template)


@task
def development(context):
    run('pip3 install -U pip')
    run('pip3 install -r requirements/development.txt')
    # _template_file('nginx/nginx.conf', '/etc/nginx/sites-enabled/default')
    # _template_file('supervisor.nginx.conf', '/etc/supervisor/conf.d/nginx.conf')
    # _template_file('supervisor.celery.conf', '/etc/supervisor/conf.d/celery.conf')
    run('supervisord -n')
