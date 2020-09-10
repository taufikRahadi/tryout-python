import click
import asyncio
import json
from Fetcher import Fetcher as fetcher
from datetime import datetime

async def fetch(city, unit, temp):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid=fb62799e9ab91167794fd4520bb139f7#'
    w = asyncio.create_task(fetcher.get(url))
    data =  await w
    datenow = datetime.now().strftime('%A %B %-d, %Y %I:%M:%S %p')
    main = list(data['main'] + ', ' +data['description'] for data in data['weather'])
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%A %B %-d, %Y %I:%M:%S %p')
    sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%A %B %-d, %Y %I:%M:%S %p')

    print(f'datetime \t: {datenow}')
    print(f'city \t \t: {data["name"]}')
    print(f'temperature\t: {data["main"]["temp"]}° {temp}')
    print(f'weather \t: {" ".join(main)}')
    print(f'sunrise \t: {sunrise}')
    print(f'sunset  \t: {sunset}')

async def classic_fetch(city, unit, tem):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid=fb62799e9ab91167794fd4520bb139f7#'
    t = await fetcher.get(url)
    main = " ".join(list(t['main'] + ', ' +t['description'] for t in t['weather']))
    print(f'{t["name"]} \t | {t["main"]["temp"]}°{tem} | {main}')

async def mul_cities(cities, tem):
    unit = 'metric'
    tasks = [classic_fetch(city, unit, tem) for city in cities]
    datenow = f"{datetime.now().strftime('%A %B %-d, %Y %I:%M:%S %p')} \t"
    print('-' * len(datenow))
    return [await task for task in tasks]

async def temp_true(city, unit, temp):
    task = asyncio.create_task(classic_fetch(city, unit, temp))
    await task

@click.command(name="weather")
@click.argument('city', nargs=-1)
@click.option('--cities', default=False, is_flag=True)
@click.option('--temp', default=False, is_flag=True)
@click.option('--celcius', is_flag=True)
@click.option('--fahrenheit', is_flag=True)
def weather(cities, city, temp, celcius, fahrenheit):
    unit = ''
    tem = 'Kelvin'
    if celcius:
        unit += 'metric'
        tem = 'Celcius'
    if fahrenheit:
        unit += 'imperal'
        tem = 'Fahrenheit'

    loop = asyncio.get_event_loop()
    if cities != True:
        if temp:
            datenow = datetime.now().strftime('%A %B %-d, %Y %I:%M:%S %p')
            print(datenow)
            print('-' * len(datenow))
            loop.run_until_complete(temp_true(city[0], unit, tem))
        else:
            loop.run_until_complete(fetch(city[0], unit, tem))
    else:
        loop.run_until_complete(mul_cities(city, tem))

if __name__ == '__main__':
    weather()
    