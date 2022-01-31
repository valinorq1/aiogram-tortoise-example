import asyncio
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN


loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN,
          loop=loop, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
