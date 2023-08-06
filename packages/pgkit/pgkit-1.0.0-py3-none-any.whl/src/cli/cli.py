import click
from cli.commands.config import config
from cli.commands.pitr import pitr
from cli.commands.status import status
from cli.commands.list import list

@click.group()
def cli():
    pass

cli.add_command(config)
cli.add_command(pitr)
cli.add_command(status)
cli.add_command(list)
