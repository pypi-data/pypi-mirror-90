import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--run_id', help='Local run identifier (covid19...)', required=True)
def command(run_id: str):
    """
    Run post-processing workflow steps
    """

    import cli.worker
    import cli.utils

    result = cli.worker.call('worker.sequencing.tasks.post_process', run_id=run_id)
    cli.utils.jprint(result)
