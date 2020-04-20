import click
from .core import validate_atom

@click.group()
def cli():
    pass

@cli.command(name="atom")
@click.argument('service-url')
@click.argument('result-path', type=click.Path(exists=True))
def validate_atom_commmand(service_url, result_path):
    validate_atom(service_url, result_path)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()