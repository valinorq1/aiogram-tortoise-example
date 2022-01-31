from aiogram.utils import executor

from bot_config import dp, loop
from config import create_pool
from admin import callbacks
from admin import handler


if __name__ == '__main__':
    loop.create_task(create_pool())
    executor.start_polling(dp, skip_updates=True)
