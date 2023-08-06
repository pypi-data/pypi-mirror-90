import click
from src.application.db import DB
import src.application.pitr as PITR

@click.group()
def pitr():
    pass

@pitr.command()
@click.argument('name', required=True)
@click.argument('delay', required=True, type=int)
def backup(name, delay):
    config = DB.get_config(name)
    PITR.backup(**{**config, 'delay': delay})

@pitr.command()
def restore():
    pass

@pitr.command()
def status():
    pass
