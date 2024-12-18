import aiohttp
from aiohttp import web
import asyncio
from handler import Handler

API_URL = "http://numbersapi.com/"

def get_primes():
    n = 1010
    lst=[2]
    for i in range(3, n+1, 2):
        if (i > 10) and (i%10==5):
            continue
        for j in lst:
            if j*j-1 > i:
                lst.append(i)
                break
            if (i % j == 0):
                break
        else:
            lst.append(i)
    return lst

async def update(request):
    """
    Handle the POST request to update the database with prime numbers.

    :param request: The HTTP request object.
    """
    numbers = get_primes()
    handler = Handler(API_URL, asyncio.get_event_loop(), request.method) 
    await handler.handle(numbers)
    raise web.HTTPOk()

async def numbers(request):
    """
    Handle the GET request to fetch trivia about numbers.

    :param request: The HTTP request object.
    """
    number = request.match_info.get('number')
    if number is not None and (not number.isdigit() or int(number) < 50 or int(number) > 1000):
        raise web.HTTPBadRequest()
    numbers = list(range(50, 1001)) if request.match_info.get('number') is None else [request.match_info.get('number')]
    handler = Handler(API_URL, asyncio.get_event_loop(), request.method) 
    await handler.handle(numbers)
    return web.Response(text=''.join([str(item) for item in handler.output]))



if __name__ == '__main__':
    app = web.Application()

    app.router.add_get('/numbers/{number}', numbers)
    app.router.add_get('/numbers', numbers)
    app.router.add_post('/numbers', update)

    web.run_app(app, port=5858)
