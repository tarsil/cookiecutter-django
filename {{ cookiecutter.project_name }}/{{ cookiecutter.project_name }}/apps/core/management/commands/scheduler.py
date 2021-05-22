import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * <command to execute>

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database.

    Args:
      max_age:  (Default value = 604_800)

    Returns:

    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    """Triggers when current time matches all specified time constraints,
    similarly to how the UNIX cron scheduler works.

    Args:
      int: str year: 4-digit year
      int: str month: month (1-12)
      int: str day: day of the (1-31)
      int: str week: ISO week (1-53)
      int: str day_of_week: number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
      int: str hour: hour (0-23)
      int: str minute: minute (0-59)
      int: str second: second (0-59)
      datetime: str start_date: earliest possible date/time to trigger on (inclusive)
      datetime: str end_date: latest possible date/time to trigger on (inclusive)
      datetime: tzinfo|str timezone: time zone to use for the date/time calculations (defaults
    to scheduler timezone)
      int: None jitter: advance or delay the job execution by ``jitter`` seconds at most.

    .. note:: The first weekday is always **monday**.

    Returns:

    """
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        """

        Args:
          *args:
          **options:

        Returns:

        """
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_old_job_executions,
            # Midnight on Monday, before start of the next work week.
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
