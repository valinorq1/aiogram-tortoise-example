import os

from tortoise import Tortoise

# bot token
TOKEN = os.environ['token']
# bot main admin
ADMIN = os.environ['admin']
# default account sleep before activate (1 month by deafult)
WAIT_PENDING_TIME = 2678400
DATABASE_URL = os.environ['db_url']

# grab all tables from all apps
INSTALLED_APPS = ['admin', 'client', 'post', 'session']
MODELS = ["{}.models".format(app) for app in INSTALLED_APPS]
MODELS.append("aerich.models")
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        },
    },
    'timezone': 'Europe/Moscow'
}


async def create_pool():
    """init db, create connection pool"""
    INSTALLED_APPS = ['admin', 'client', 'post', 'session']
    MODELS = ["{}.models".format(app) for app in INSTALLED_APPS]

    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': MODELS},
        timezone="Europe/Moscow"
    )
    await Tortoise.generate_schemas()
