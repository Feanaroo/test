import unittest
import asyncio
import aiohttp
import sys

sys.path.insert(0, '..')

import handler

class Test(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
 
    def tearDown(self):
        self.loop.close()

    def test_api(self):
        test_handler = handler.Handler('http://numbersapi.com/', self.loop, 'GET')
        async def go():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                await test_handler.download_json_coroutine(session, 100, test_handler.url)
        self.loop.run_until_complete(go())
        self.assertTrue(test_handler.output.pop()['found'])

    def test_handle(self):
        test_handler = handler.Handler('http://numbersapi.com/', self.loop, 'GET')
        async def go():
            await test_handler.handle([100])
        self.loop.run_until_complete(go())
        self.assertTrue(test_handler.output.pop()['found'])

    def test_post(self):
        test_handler = handler.Handler('http://numbersapi.com/', self.loop, 'POST')
        async def go():
            await test_handler.handle([100])
        self.loop.run_until_complete(go())
        self.assertEqual(len(test_handler.output), 1)

    def test_download_xml_coroutine(self):
        test_handler = handler.Handler('http://numbersapi.com/', self.loop, 'GET')
        async def go():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                await test_handler.download_xml_coroutine(session, 100, test_handler.url)
        self.loop.run_until_complete(go())
        self.assertTrue(test_handler.output.pop().tag == 'number')

    def test_handle_xml(self):
        test_handler = handler.Handler('http://numbersapi.com/', self.loop, 'GET')
        async def go():
            await test_handler.handle([100])
        self.loop.run_until_complete(go())
        self.assertTrue(test_handler.output.pop().tag == 'number')

    def test_broken_xml(self):
        test_handler = handler.Handler('http://numbersapi.com/', self.loop, 'GET')
        async def go():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                try:
                    await test_handler.download_xml_coroutine(session, 999999, test_handler.url)
                except ET.ParseError:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
        self.loop.run_until_complete(go())

if __name__ == "__main__":
    unittest.main()
