import unittest
import asyncio
import aiohttp

#я проиграл директориям
sys.path.insert(0,'..')

import handler

class Test(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
 
    def tearDown(self):
        pass

    def test_api(self):
        test_handler = handler.Handler('http://numbersapi.com/', self.loop, 'GET')
        async def go():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                await test_handler.download_json_coroutine(session, 100, test_handler.url)
        self.loop.run_until_complete(go())
        self.assertTrue(test_handler.output.pop()['found'])

if __name__ == "__main__":
    unittest.main()
