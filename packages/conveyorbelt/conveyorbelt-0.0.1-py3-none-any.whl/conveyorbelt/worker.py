import logging

import celery

LOGGER = logging.getLogger(__name__)


def call(task: str, *args, **kwargs):
    """
    Run a task on the worker synchronously (wait until the result is returned)

    @param task: Module name of the task e.g. 'worker.tasks.get_config'
    @param args: The arguments for the task
    @param kwargs: The keyword arguments for the task
    @return: The result of the task
    """

    producer = celery.Celery()

    LOGGER.info("Calling task '%s'", task)
    LOGGER.debug("args=%s", args)
    LOGGER.debug("kwargs=%s", kwargs)

    result = producer.send_task(task, args=args, kwargs=kwargs)

    LOGGER.info("Celery task ID: '%s'", result.id)

    return result.get()
