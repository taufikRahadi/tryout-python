import click
import asyncio
from Fetcher import Fetcher as fetcher
import json
from datetime import datetime
# from functools import wraps

async def fetch(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid=fb62799e9ab91167794fd4520bb139f7'
    data = await fetcher.get(url)
    return data

async def fetch_data(city):
    data = asyncio.create_task(fetch(city))
    return await data

def process_dt(dt):
    return datetime.utcfromtimestamp(dt).strftime('%Y %m %d') == datetime.now().strftime('%Y %m %d')

@click.command(name="forecast")
@click.option('--days', is_flag=True)
@click.argument('city')
def forecast(days, city):
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_data(city))
    datenow = datetime.now().strftime('%A %B %-d, %Y %I:%M:%S %p')
    print(datenow)
    print('-' * 50)
    data = list(d for d in data['list'] if process_dt(d['dt']))
    for d in data:
        main = " ".join(list(d['main'] + ', ' +d['description'] for d in d['weather']))
        print(f'{datetime.fromtimestamp(d["dt"]).strftime("%I:%M %p")} | {d["main"]["temp"]}° Celcius | {main}')

if __name__ == '__main__':
    forecast()
