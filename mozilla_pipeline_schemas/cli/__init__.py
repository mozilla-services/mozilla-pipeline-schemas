import click
from .bigquery import bigquery


@click.group()
def mps():
    pass


mps.add_command(bigquery)
