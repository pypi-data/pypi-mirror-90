import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--run_id', help='Local run identifier "covid19-2020-..."', required=True)
def command(run_id: str):
    """
    Transfer data from the sequencer to the HPC
    """

    import cli.worker
    import cli.utils

    protocol_run = cli.worker.call('worker.sequencing.tasks.get_protocol_run_info', run_id=run_id)
    cli.utils.jprint(protocol_run)
    result = cli.worker.call('worker.minknow.tasks.transfer_data', run_id=run_id, protocol_run=protocol_run)
    cli.utils.jprint(result)
    result = cli.worker.call('worker.sequencing.tasks.move_finished', run_id=run_id, protocol_run=protocol_run)
    cli.utils.jprint(result)
