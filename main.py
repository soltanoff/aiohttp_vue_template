import aiohttp_jinja2
import jinja2
from aiohttp import web

import settings
from routers import index, articles

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRECTORY))
app.router.add_static(settings.STATIC_URL, path=settings.STATIC_DIRECTORY, name='static')
app.add_routes(index.router)
app.add_routes(articles.router)

if __name__ == '__main__':
    web.run_app(app)
