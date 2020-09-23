import click
from .bigquery import bigquery


@click.group()
def entry_point():
    pass


entry_point.add_command(bigquery)
