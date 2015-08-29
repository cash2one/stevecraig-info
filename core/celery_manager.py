import os 

from celery import Celery

includes = []

for task_file in os.listdir('tasks'):
    if task_file.endswith('_task.py'):
        task_module = 'tasks.' + task_file.split('.py', 1)[0]
        includes.append(task_module)

app = Celery('butl',
             broker = 'amqp://guest@localhost',
             backend = 'amqp://',
             include = includes)

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)