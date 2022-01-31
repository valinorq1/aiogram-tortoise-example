import os


from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from aiogram.types import InputTextMessageContent, InlineQueryResult, InlineKeyboardMarkup, InlineKeyboardButton

from .keyboard.settings_inline import get_settings_inline
from .keyboard.keyboards import admin_keyboard
from bot_config import dp, loop, bot


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply('Глобальные настройки', reply_markup=get_settings_inline())


@dp.message_handler(commands=['admin'])
async def cmd_admin(message: types.Message):
    await message.reply('Админ панель', reply_markup=admin_keyboard())


@dp.message_handler(filters.Text(equals=['♻ Настройки']))
async def show_global_settings(m: types.Message):
    await bot.send_message(m.chat.id, "Глобальные настройки", reply_markup=await get_settings_inline())
