
import os

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
    """
    Development environment
    """
    run('pip3 install -U pip')
    run('make requirements-dev')
    run('pre-commit install')
    run('supervisord -n')


@task
def testing(context):
    """
    For the unittesting in our CI
    """
    run('make requirements-dev')
    run('make test DB=--create-db')


@task
def pgbouncer(context):
    """
    PG Bouncer to run in the local development
    """
    _template_file("pgbouncer/dev/pgbouncer.ini", "/tmp/pgbouncer.ini")
    command = "/usr/sbin/pgbouncer -u www-data /tmp/pgbouncer.ini"
    # run("apt-get update")
    run("apt-get install -y libc-ares2")
    run("chmod +x /usr/sbin/pgbouncer")
    run(command)
