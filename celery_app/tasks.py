import os
import time
import uuid
from celery import Celery
import sys
import logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__) 
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'simple': {
#             'format': '%(levelname)s %(message)s',
#              'datefmt': '%y %b %d, %H:%M:%S',
#             },
#         },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'celery': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'celery.log',
#             'formatter': 'simple',
#             'maxBytes': 1024 * 1024 * 100,  # 100 mb
#         },
#     },
#     'loggers': {
#         'celery': {
#             'handlers': ['celery', 'console'],
#             'level': 'DEBUG',
#         },
#     }
# }

# from logging.config import dictConfig
# dictConfig(LOGGING)


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(120)
    return x + y

@celery.task(name='tasks.generate_codes')
def generate_codes(number_of_codes: int) -> []:
    codes = {}
    return_codes = []

    logger.info("Creating - " + str(number_of_codes) + " codes, this may take a minute.")
    #will probably need to check all existing codes to ensure that we arent reusing.
    #using pythons uuid lib 
    while len(codes) < number_of_codes:
        code = str(uuid.uuid4())
        try:
            codes[code]
        except KeyError:
            codes[code] = 1 
            return_codes.append(code)
            
    return return_codes
