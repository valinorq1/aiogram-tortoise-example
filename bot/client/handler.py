import os


from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from aiogram.types import InputTextMessageContent, InlineQueryResult, InlineKeyboardMarkup, InlineKeyboardButton

from bot_config import dp, loop, bot


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply('Глобальные настройки', reply_markup=get_settings_inline())
