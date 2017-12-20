import os
import sys

from jinja2 import Environment, FileSystemLoader
from invoke import run, task


@task
def development(context):
    run('pip3 install -U pip')
    run('pip3 install -r requirements/development.txt')
    run('supervisord -n')
