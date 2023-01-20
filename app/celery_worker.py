from celery import Celery
from celery.utils.log import get_task_logger
from celery.exceptions import MaxRetriesExceededError
from captcha_2 import jump_captcha

# Initialize celery with RabbitMQ
celery = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672//')
celery_log = get_task_logger(__name__)

@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 1})
def create_order(self,name, url):
    try:
        data_ssalud = jump_captcha(url)

        if data_ssalud is not None:
            celery_log.info(f"Work Completed!")
            return {"message": f"Hi {name}, Your certificate has been validated"}
        else:
            raise Exception('Validation failed. Trying again.')

    except MaxRetriesExceededError as e:
            print(e)
            return {"message": f"Hi {name}, Your certificate could not be validated"}