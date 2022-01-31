import asyncio

from tortoise import Tortoise

from config import DATABASE_URL
from admin.models import StaticText, GlobalSettings, Manager


async def init_settings():
    """Инициализация полей и таблиц"""
    INSTALLED_APPS = ['admin', 'client', 'post', 'session']
    MODELS = ["{}.models".format(app) for app in INSTALLED_APPS]

    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': MODELS},
        timezone="Europe/Moscow"
    )
    await Tortoise.generate_schemas()
    try:
        # await Manager.create(telegram_username="val1n0r", telegram_id=647310559, role='admin')
        # await Manager.create(telegram_username="@Hermes_Service", telegram_id=5089194224, role='admin')
        await Manager.create(telegram_username="@val1n0r", telegram_id=647310559, role='admin')
    except:
        pass

    try:
        await GlobalSettings.all().delete()
    except:
        pass
    try:
        await GlobalSettings.create()
    except:
        pass
    try:
        current_static = await StaticText.first()
        if current_static:
            if current_static.rules is None:
                current_static.rules = 'Правила'
                await current_static.save()
            pass
        else:
            await StaticText.create()
    except:
        pass


asyncio.run(init_settings())
