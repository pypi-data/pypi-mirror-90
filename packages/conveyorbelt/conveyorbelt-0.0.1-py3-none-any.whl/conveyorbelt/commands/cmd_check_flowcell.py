import logging

import json
import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--id', help='Check flow cell free barcodes', required=True)
def command(id: str):
    """
    Update the assay status base on a metadata key and its value, option to update child assays too
    """

    import cli.worker
    import cli.utils


    result = cli.worker.call(
        'worker.db.tasks.check_flowcell',
        id=id,

    )
    cli.utils.jprint(result)
