import argparse

import aiohttp_jinja2
import jinja2
from aiohttp import web

import settings
from api import index, articles

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRECTORY))
app.router.add_static(settings.STATIC_URL, path=settings.STATIC_DIRECTORY, name='static')
index.setup_router(app)
articles.setup_router(app)

parser = argparse.ArgumentParser(description="CRUD App: Vue.js & aiohttp")
parser.add_argument('--host')
parser.add_argument('--port')

if __name__ == '__main__':
    args = parser.parse_args()
    web.run_app(app, host=args.host, port=args.port)
