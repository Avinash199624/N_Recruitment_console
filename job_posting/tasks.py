from datetime import timedelta, time, datetime
from django.utils import timezone
from django.utils.timezone import make_aware
import logging

from job_posting.models import JobPosting

today = timezone.now()
tomorrow = today + timedelta(1)
today_start = make_aware(datetime.combine(today, time()))
today_end = make_aware(datetime.combine(tomorrow, time()))

logger = logging.getLogger(__name__)


def change_job_posting_status():

    scheduled_job_posting = JobPosting.objects.filter(
        publication_date__range=(today_start, today_end),
        status=JobPosting.SCHEDULED)
    if scheduled_job_posting:
        for job in scheduled_job_posting:
            job.status = JobPosting.PUBLISHED
            job.save()
            logger.info(f"status changes=d to {JobPosting.PUBLISHED} for {job.__dict__}")
    else:
        logger.info(f"No Jobs to be {JobPosting.PUBLISHED}")

    published_job_posting = JobPosting.objects.filter(
        end_date__range=(today_start, today_end),
        status=JobPosting.PUBLISHED)
    if published_job_posting:
        for job in published_job_posting:
            job.status = JobPosting.SUSPENDED
            job.save()
            logger.info(f"status changes=d to {JobPosting.SUSPENDED} for {job.__dict__}")
    else:
        logger.info(f"No Jobs to be {JobPosting.SUSPENDED}")