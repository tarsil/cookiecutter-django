CELERY_TASK_ROUTES = (
    {'example.task_name': {
        'queue': '{{ project_name }}',
        'routing_key': '{{ project_name }}'
    }},
)
