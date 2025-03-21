from aiohttp import web
import os

class HTTPServer:
    def __init__(self, host: str, port: int):
        self.app = web.Application()
        self.host = host
        self.port = port
        self.app.router.add_get('/', self.health_check)

    async def health_check(self, request):
        return web.Response(text="OK")

    async def run_server(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

def start_http_server():
    port = int(os.getenv('PORT', 8080))
    http_server = HTTPServer(host='0.0.0.0', port=port)
    return http_server.run_server()
