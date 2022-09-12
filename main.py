import asyncio

import aiofiles
import aiohttp
import excel2img
from bs4 import BeautifulSoup


async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'http://students.perm.hse.ru/timetable/') as response:
            parsed = await response.text()
    soup = BeautifulSoup(parsed, 'html.parser')
    result = soup.find('div', class_='content__inner post__text')
    bakalavr_timesheet = BeautifulSoup(
        str(result).replace('Бакалавриат', 'STOP').replace('Магистратура',
                                                           'STOP').split(
            'STOP')[1],
        'html.parser')

    bakal = bakalavr_timesheet.find_all('a')
    sheets = {}
    for i in bakal:
        name = i.text

        link = i.get('href')
        if 'www.hse.ru' in link:
            link = 'http:' + link
        else:
            link = 'http://www.hse.ru' + link
        sheets[name] = link
    return sheets


async def download_sheet(name, link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            file = await aiofiles.open(f'sheets/{name}.xls', 'wb')
            await file.write(await response.read())
    await session.close()
    await file.close()


"""
async def create_picture(name):
    try:
        excel2img.export_img(f"sheets/{name}.xls",
                             f"sheets_pics/{name}.png", "1 курс", "A1:F36")
    except:
        print('Error in making picture')
        excel2img.export_img(f"sheets/{name}.xls",
                             f"sheets_pics/{name}.png")
"""

