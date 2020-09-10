from Fetcher import Fetcher as fetcher
import asyncio
import click
import json

async def fetch(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&%20units=metric&appid=fb62799e9ab91167794fd4520bb139f7'
    data = await fetcher.get(url)
    print(data)

def search_city(city):
    with open('city.id.json', 'r') as cities:
        data = json.loads(cities.read())
    print(next(d for d in data if d['name'].lower() == city.lower()))

def single_fetch(city):
    pass

def multi_fetch(city):
    pass

@click.command(name="dailyforecast")
@click.argument('city', nargs=-1)
def dailyforecast(city):
    print(search_city(city[0]))

if __name__ == '__main__':
    dailyforecast()
