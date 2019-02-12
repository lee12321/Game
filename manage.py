from celery.schedules import crontab

from apps import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from apps.blog.celery_task import make_celery
from apps.models import db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
celery = make_celery(app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@celery.task
def test(arg):
    print(arg)


if __name__ == '__main__':
    # print(app.url_map)
    manager.run()
