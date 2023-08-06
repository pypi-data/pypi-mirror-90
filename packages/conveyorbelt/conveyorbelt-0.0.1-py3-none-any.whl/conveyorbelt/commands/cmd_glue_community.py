import logging

import json
import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--date', help='Date in format 2020-11-30', required=True, default="today")
def command(date: str = 'today'):
    """
    Start the hoci community sequences task
    """

    import cli.worker
    import cli.utils

    result = cli.worker.call(
        'worker.reporting.tasks.community_seqs',
        date=date
    )
    cli.utils.jprint(result)
