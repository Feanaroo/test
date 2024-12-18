import async_timeout
import db
import json
import aiohttp
import asyncio
import xml.etree.ElementTree as ET

DAYS_AGO = 2
CLOSEST_NUMBERS_COUNT = 2

class Handler():

    def __init__(self, url, loop, method):
        self.url = url
        self.loop = loop
        self.method = method
        self.output = []

    async def handle(self, numbers):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            tasks = [self.download_json_coroutine(session, number, self.url) for number in numbers]
            await asyncio.gather(*tasks)
            # работа с БД ведётся отдельно от запросов к API, чтобы не блокировать event loop
            if self.method == 'POST':
                db.Result.upload(self.output) 
            if self.method == 'GET':
                for item in self.output:
                    rows_closest = db.Result.get_closest(item['number'], DAYS_AGO, CLOSEST_NUMBERS_COUNT)
                    viewer = db.ResultViewer(rows_closest)
                    item['primes'] = viewer.output_json(CLOSEST_NUMBERS_COUNT)

    async def download_json_coroutine(self, session, number, url):
        url = str(url) + str(number) + "?json"
        with async_timeout.timeout(20):
            async with session.get(url) as response:
                json_str = await response.content.read()
                output = json.loads(json_str)
                self.output.append(output)
                return await response.release()

    async def download_xml_coroutine(self, session, number, url):
        url = str(url) + str(number) + "?xml"
        with async_timeout.timeout(20):
            async with session.get(url) as response:
                xml_str = await response.content.read()
                output = ET.fromstring(xml_str)
                self.output.append(output)
                return await response.release()
