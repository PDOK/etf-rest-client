import json
import click
from .core import validate_service


@click.group()
def cli():
    pass


@cli.command(name="validate-service")
@click.argument('service-type')
@click.argument('service-url')
@click.argument('result-path', type=click.Path(exists=True))
@click.option('--validator-url')
def validate_atom_commmand(
        service_type, service_url, result_path, validator_url):
    result = validate_service("ATOM", service_url, result_path, validator_url)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
