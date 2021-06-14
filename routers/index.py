import aiohttp_jinja2
from aiohttp import web

import settings


router = web.RouteTableDef()


@router.get('/')
@aiohttp_jinja2.template(settings.BASE_TEMPLATE_NAME)
async def index(request):
    return {'request': request, 'csrf_token': 'TODO'}
