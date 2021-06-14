from aiohttp_remotes import AllowedHosts

import settings


def setup_middlewares(app):
    app.middlewares.append(ALLOWED_HOST_MIDDLEWARE.middleware)


ALLOWED_HOST_MIDDLEWARE = AllowedHosts(allowed_hosts=settings.ALLOWED_HOSTS)
