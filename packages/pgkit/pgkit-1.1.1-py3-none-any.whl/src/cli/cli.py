import click
from src.cli.commands.config import config
from src.cli.commands.pitr import pitr
from src.cli.commands.status import status
from src.cli.commands.list import list

@click.group()
def cli():
    pass

def main():
    cli.add_command(config)
    cli.add_command(pitr)
    cli.add_command(status)
    cli.add_command(list)
    cli()
