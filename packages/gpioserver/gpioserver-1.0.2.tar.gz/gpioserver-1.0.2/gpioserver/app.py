from aiohttp import web

from functools import partial

from gpioserver.gpio import DebugGPIO, RaspberryGPIO

import asyncio

def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]

def get_commands(request):
    for cmd, value in partition(request.match_info["commands"].strip("/").split("/"), 2):
        yield cmd, int(value)

class GPIOBackend(object):
    def __init__(self, gpio, gpio_modes=None, max_wait = None):
        self.gpio = gpio
        self.gpio_modes = {i: "input" for i in range(1, 27)}

        if isinstance(gpio_modes, (tuple, list)):
            gpio_modes = dict(gpio_modes)


        self.gpio_modes.update(gpio_modes or {})

        for n, mode in self.gpio_modes.items():
            self.gpio.setup(mode, n)

        self.max_wait = max_wait or 2000

    async def wait(self, milliseconds):
        wait = max(0, min(milliseconds, self.max_wait))
        if wait:
            await asyncio.sleep(wait / 1000)
        return wait

    async def high(self, n):
        return await self.gpio.output(self.assert_output(n), high=True)

    async def low(self, n):
        return await self.gpio.output(self.assert_output(n), high=False)

    async def read(self, n):
        return await self.gpio.input(self.assert_input(n))

    def get_all_input(self):
        return filter(self.is_input, self.gpio_modes.keys())

    def get_all_output(self):
        return filter(self.is_output, self.gpio_modes.keys())

    def is_output(self, n):
        try:
            return self.gpio_modes[n].startswith("output")
        except KeyError:
            return False

    def is_input(self, n):
        try:
            return self.gpio_modes[n].startswith("input")
        except KeyError:
            return False

    def assert_output(self, n):
        if not self.is_output(n):
            raise ValueError("Not an output pin")
        return n

    def assert_input(self, n):
        if not self.is_input(n):
            raise ValueError("Not an input pin")
        return n

    async def run_commands(self, commands):
        results = []
        for cmd, value in commands:
            results.append(await self.run_command(cmd, value))
        return results

    async def run_command(self, cmd, value, **opts):
        try:
            return {
                "command": cmd,
                "argument": value,
                "result": await getattr(self, cmd)(value, **opts),
            }
        except Exception as e:
            return {
                "command": cmd,
                "argument": value,
                "error": e.__class__.__name__,
                "message": str(e),
            }

def api_response(results = (), **opts):
    status = any(r.get("error", None) for r in results) and 500 or 200

    return web.json_response({"status": status, **opts}, status=status)

async def command(request, backend):

    results = await backend.run_commands(get_commands(request))

    return api_response(results, commands = results)

async def status(request, backend):

    results = await backend.run_commands((("read", id) for id in backend.get_all_input()))

    return api_response(results, input = {r["argument"]: r["result"] for r in results if not "error" in r})

async def home(request, backend):

    return api_response(input = tuple(backend.get_all_input()), output = tuple(backend.get_all_output()))


def create_app(debug=False, mode=None, max_wait=None, gpio_modes = None):

    backend = GPIOBackend(
        gpio=(debug and DebugGPIO or RaspberryGPIO)(mode=mode),
        gpio_modes=gpio_modes,
        max_wait=max_wait,
    )

    app = web.Application()
    app.add_routes(
        [
            web.get(
                r"/{commands:((wait|high|low|read)/[0-9]+/)+}",
                partial(command, backend=backend),
            )
        ]
    )
    app.add_routes([web.get(r"/status/", partial(status, backend=backend))])
    app.add_routes([web.get(r"/", partial(home, backend=backend))])

    return app

def run_app(port=None, host=None, **opts):
    return web.run_app(create_app(**opts), port=port, host=host or "0.0.0.0")