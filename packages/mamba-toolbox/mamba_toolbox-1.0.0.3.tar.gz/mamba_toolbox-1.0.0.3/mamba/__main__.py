import click
from .commands import new_project

@click.group()
def cli():
    pass

cli.add_command(new_project)



if __name__ == "__main__":
    cli()
