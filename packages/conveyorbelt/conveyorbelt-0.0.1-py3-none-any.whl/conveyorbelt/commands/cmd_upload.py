import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--run_id', help='Local run identifier (covid19...)', required=True)
@click.option('--api_token', help='majora api token', required=True)
def command(run_id: str, api_token: str):
    """
    Upload run to climb
    """

    import cli.worker
    import cli.utils


    result = cli.worker.call(
        'worker.dissemination.tasks.disseminate',
        dry_run=False,
        run_id=run_id,
        api_token=api_token
        )
    cli.utils.jprint(result)
