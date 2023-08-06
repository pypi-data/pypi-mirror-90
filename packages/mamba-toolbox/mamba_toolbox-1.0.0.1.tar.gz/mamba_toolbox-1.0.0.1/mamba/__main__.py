import click
from .commands import new_project

@click.group()
def cli():
    pass

cli.add_command(new_project)



if __name__ == "__main__":
    print('Mamba tools v'+'.'.join(str(x) for x in __version__))
    cli()
