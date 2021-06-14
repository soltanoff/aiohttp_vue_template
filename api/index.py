import aiohttp_jinja2

import settings


def setup_router(app):
    app.router.add_view("/", index)


@aiohttp_jinja2.template(settings.BASE_TEMPLATE_NAME)
async def index(request):
    return {'request': request, 'csrf_token': 'TODO'}
