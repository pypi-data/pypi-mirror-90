import json
import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
def command():
    """
    Get worker configuration
    """

    import cli.worker

    result = cli.worker.call('worker.tasks.get_config')
    print(json.dumps(result, indent=2))
