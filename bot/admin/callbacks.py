import typing

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from admin.keyboard.settings_inline import get_settings_inline, settings_cb
from bot_config import bot, loop, dp
from admin.models import GlobalSettings
from admin.states import (EditGlobalMessageIntervalState, EditGlobalLoopIntervalState,
                          UpdateWelcomeText, UpdateSupportText, UpdateRulesText, UpdateLoopMessageLimit,
                          UpdateChatsList)


@dp.callback_query_handler(settings_cb.filter(action=['self_run_on', 'self_run_off']))
async def query_self_run(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """switch self run user ad"""
    callback_data_action = callback_data['action']
    if callback_data_action == 'self_run_off':
        await GlobalSettings.first().update(allow_self_run=False)
        await bot.edit_message_text(
            f'Выключили самозапуск',
            query.from_user.id,
            query.message.message_id,
            reply_markup=await get_settings_inline(),
        )
        await bot.answer_callback_query(query.id, "Выключили самозапуск", show_alert=True)
    elif callback_data_action == 'self_run_on':
        await GlobalSettings.first().update(allow_self_run=True)
        await bot.edit_message_text(
            f'<b>Включили самозапуск</b>',
            query.from_user.id,
            query.message.message_id,
            reply_markup=await get_settings_inline(),
        )
        await bot.answer_callback_query(query.id, "Включили самозапуск", show_alert=True)
    await query.answer()


@dp.callback_query_handler(settings_cb.filter(action=['moderation_on', 'moderation_off']))
async def query_moderation_status(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """switch moderation status"""
    callback_data_action = callback_data['action']
    if callback_data_action == 'moderation_off':
        await GlobalSettings.first().update(enable_moderation=False)
        await bot.edit_message_text(
            f'Выключили премодерацию',
            query.from_user.id,
            query.message.message_id,
            reply_markup=await get_settings_inline(),
        )
        await bot.answer_callback_query(query.id, "Успешно выключили премодерацию", show_alert=True)
    elif callback_data_action == 'moderation_on':
        await GlobalSettings.first().update(enable_moderation=True)
        await bot.edit_message_text(
            f'Включили премодерацию',
            query.from_user.id,
            query.message.message_id,
            reply_markup=await get_settings_inline(),
        )
        await bot.answer_callback_query(query.id, "Успешно включили премодерацию", show_alert=True)
    await query.answer()


@dp.callback_query_handler(settings_cb.filter(action=['int_message', 'int_loop']))
async def query_interval(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """set new interval for global sender"""
    await query.answer()
    if callback_data['action'] == 'int_message':
        await bot.delete_message(query.from_user.id, query.message.message_id)
        await bot.send_message(query.from_user.id, "Введите новый интервал между сообщениями:")
        await EditGlobalMessageIntervalState.new_message_interval.set()
    elif callback_data['action'] == 'int_loop':
        await bot.delete_message(query.from_user.id, query.message.message_id)
        await EditGlobalLoopIntervalState.new_loop_interval.set()
        await bot.send_message(query.from_user.id, "Введите новый цикловый интервал:")


@dp.callback_query_handler(settings_cb.filter(action=['welcome_text']))
async def query_set_new_welcome_text(query: types.CallbackQuery):
    """set new text for /start command"""
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await bot.send_message(query.from_user.id, "Введите новый текст для команды /start")
    await UpdateWelcomeText.new_text.set()


@dp.callback_query_handler(settings_cb.filter(action=['support_text']))
async def query_set_new_support_text(query: types.CallbackQuery):
    """set new text for /start command"""
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await bot.send_message(query.from_user.id, "Введите новый текст для кнопки ПОДДЕРЖКА:")
    await UpdateSupportText.new_text.set()


@dp.callback_query_handler(settings_cb.filter(action=['rules_text']))
async def query_set_new_rules_text(query: types.CallbackQuery):
    """set new text for rules command"""
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await bot.send_message(query.from_user.id, "Введите новый текст для кнопки ПРАВИЛА:")
    await UpdateRulesText.new_text.set()


@dp.callback_query_handler(settings_cb.filter(action=['message_per_loop']))
async def query_set_loop_message_limit(query: types.CallbackQuery):
    """set new limit for global loop"""
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await bot.send_message(query.from_user.id, "Укажите новый лимит сообщениий за цикл рассылки:")
    await UpdateLoopMessageLimit.new_limit.set()


@dp.callback_query_handler(settings_cb.filter(action=['global_chats']))
async def query_update_global_chats(query: types.CallbackQuery):
    """update chats list with timeout"""
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await bot.send_message(query.from_user.id, "Отправь мне обновлённый файл с чатами:")
    await UpdateChatsList.new_chat_file.set()


@dp.errors_handler(exception=MessageNotModified)  # for skipping this exception
async def message_not_modified_handler(update, error):
    return True
