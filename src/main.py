from src.weather import weather
from src.forecast import forecast
import click

@click.group()
def cli():
    pass

cli.add_command(weather)
cli.add_command(forecast)

if __name__ == '__main__':
    cli()
