import math

from aiohttp import web
from sqlalchemy import func, select

import settings
from tables import database, ArticlesTable

router = web.RouteTableDef()


@router.get('/api/article/')
async def get_articles(request):
    query = ArticlesTable.select()
    page = int(request.rel_url.query.get('page', 1))
    articles = await database.fetch_all(query.limit(settings.PAGE_SIZE).offset((page - 1) * settings.PAGE_SIZE))
    total_articles_count = await database.fetch_val(select([func.count()]).select_from(ArticlesTable))
    return web.json_response({
        'pages_info': [
            {
                'number': number,
                'link': f'/api/article/?page={number}'
            }
            for number in range(1, int(math.ceil(total_articles_count / float(settings.PAGE_SIZE))) + 1)
        ],
        'articles': [dict(zip(["id", "title", "content"], list(article))) for article in articles]
    })


@router.get('/api/article/{item_id}/')
async def get_article_by_id(request):
    item_id = int(request.match_info['item_id'])
    query = ArticlesTable.select()
    article = await database.fetch_one(query.where(ArticlesTable.columns.id == item_id))
    return web.json_response(dict(zip(["id", "title", "content"], list(article))))


@router.post('/api/article/')
async def create_article(request):
    article = await request.json()
    query = ArticlesTable.insert().values(title=article['title'], content=article['content'])
    await database.execute(query)
    return web.Response()


@router.put('/api/article/{item_id}/')
async def update_article_by_id(request):
    item_id = int(request.match_info['item_id'])
    article = await request.json()
    query = ArticlesTable.update().values(title=article['title'], content=article['content'])
    result_success = await database.execute(query.where(ArticlesTable.columns.id == item_id))
    if result_success:
        return web.json_response(dict(id=item_id, title=article['title'], content=article['content']))
    raise web.HTTPInternalServerError(reason="The article could not be saved")


@router.delete('/api/article/{item_id}/')
async def delete_article_by_id(request):
    item_id = int(request.match_info['item_id'])
    query = ArticlesTable.delete()
    await database.execute(query.where(ArticlesTable.columns.id == item_id))
    return web.Response()
