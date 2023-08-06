import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
# @click.option('--run_id', help='Local run identifier (covid19...)', required=True)
# @click.option('--protocol_run_id', help='Sequencer job identifier', required=True)
def command():


    import cli.worker
    import cli.utils

    result = cli.worker.call('worker.dissemination.tasks.phe')
    cli.utils.jprint(result)
