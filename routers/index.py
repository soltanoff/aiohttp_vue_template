import aiohttp_jinja2

import settings


def setup_routes(app):
    app.router.add_get('/', index)


@aiohttp_jinja2.template(settings.BASE_TEMPLATE_NAME)
async def index(request):
    return {'request': request, 'csrf_token': 'TODO'}
