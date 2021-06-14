import math

from aiohttp import web
from aiohttp_pydantic import PydanticView
from sqlalchemy import func, select

import models
import settings
from tables import database, ArticlesTable


def setup_router(app):
    app.router.add_view("/api/article/", ArticleCollectionView)
    app.router.add_view("/api/article/{item_id}/", ArticleItemView)


class ArticleCollectionView(PydanticView):

    async def get(self, page: int = 1):
        page = page or 1
        query = ArticlesTable.select()
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

    async def post(self, article: models.ArticleIn):
        query = ArticlesTable.insert().values(title=article.title, content=article.content)
        await database.execute(query)
        return web.Response()


class ArticleItemView(PydanticView):

    async def get(self, item_id: int, /):
        query = ArticlesTable.select()
        article = await database.fetch_one(query.where(ArticlesTable.columns.id == item_id))
        return web.json_response(dict(zip(["id", "title", "content"], list(article))))

    async def put(self, item_id: int, /, article: models.ArticleIn):
        query = ArticlesTable.update().values(title=article.title, content=article.content)
        result_success = await database.execute(query.where(ArticlesTable.columns.id == item_id))
        if result_success:
            return web.json_response(dict(id=item_id, title=article.title, content=article.content))
        raise web.HTTPInternalServerError(reason="The article could not be saved")

    async def delete(self, item_id: int, /):
        query = ArticlesTable.delete()
        await database.execute(query.where(ArticlesTable.columns.id == item_id))
        return web.Response()
