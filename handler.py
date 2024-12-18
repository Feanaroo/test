import async_timeout
import db
import json
import aiohttp
import asyncio

DAYS_AGO = 2
CLOSEST_NUMBERS_COUNT = 2

class Handler():
    """
    Handler class to manage the interaction with the Numbers API and the database.
    """

    def __init__(self, url, loop, method):
        """
        Initialize the Handler object.

        :param url: The base URL of the Numbers API.
        :param loop: The event loop to be used for asynchronous operations.
        :param method: The HTTP method (GET or POST) to be used for the requests.
        """
        self.url = url
        self.loop = loop
        self.method = method
        self.output = []

    async def handle(self, numbers):
        """
        Handle the processing of the given numbers.

        :param numbers: A list of numbers to be processed.
        """
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
        """
        Download JSON data for the given number from the Numbers API.

        :param session: The aiohttp ClientSession to be used for the request.
        :param number: The number for which to fetch the data.
        :param url: The base URL of the Numbers API.
        """
        url = str(url) + str(number) + "?json"
        with async_timeout.timeout(20):
            async with session.get(url) as response:
                json_str = await response.content.read()
                output = json.loads(json_str)
                self.output.append(output)
                return await response.release()
