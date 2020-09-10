from src.weather import weather
import click

@click.group()
def cli():
    pass

cli.add_command(weather())

if __name__ == '__main__':
    cli()
