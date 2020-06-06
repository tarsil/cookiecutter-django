CELERY_TASK_ROUTES = (
    {'example.task_name': {
        'queue': '{{ cookiecutter.project_name }}',
        'routing_key': '{{ cookiecutter.project_name }}'
    }},
)
