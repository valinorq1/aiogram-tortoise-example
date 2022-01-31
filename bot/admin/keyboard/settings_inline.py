from aiogram import md, types
from aiogram.utils.callback_data import CallbackData

from admin.models import GlobalSettings

settings_cb = CallbackData('settings', 'action')


async def get_settings_inline() -> types.InlineKeyboardMarkup:
    """
    Global settings inline
    """
    settings = await GlobalSettings.first()
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    if settings.allow_self_run:
        buttons.append(types.InlineKeyboardButton(
            "Самозапуск ✅", callback_data=settings_cb.new(action='self_run_off')))
    else:
        buttons.append(types.InlineKeyboardButton(
            "Самозапуск 🅾", callback_data=settings_cb.new(action='self_run_on')))
    if settings.enable_moderation:
        buttons.append(types.InlineKeyboardButton(
            "Премодерация ✅", callback_data=settings_cb.new(action='moderation_off')))
    else:
        buttons.append(types.InlineKeyboardButton(
            "Премодерация 🅾", callback_data=settings_cb.new(action='moderation_on')))

    buttons.append(types.InlineKeyboardButton(
        f"🕑Инт.смс ({settings.message_interval_min}-{settings.message_interval_max})",
        callback_data=settings_cb.new(action='int_message')))
    buttons.append(types.InlineKeyboardButton(
        f"🕑 Инт. цикл ({settings.loop_interval_min}-{settings.loop_interval_max})", callback_data=settings_cb.new(action='int_loop')))
    buttons.append(types.InlineKeyboardButton(f"📜 Приветствие",
                   callback_data=settings_cb.new(action='welcome_text')))
    buttons.append(types.InlineKeyboardButton(
        f"📜 Поддержка", callback_data=settings_cb.new(action='support_text')))
    buttons.append(types.InlineKeyboardButton(
        f"📜 Правила", callback_data=settings_cb.new(action='rules_text')))
    buttons.append(types.InlineKeyboardButton(f"🔁 Смс за цикл ({settings.message_limit})",
                   callback_data=settings_cb.new(action='message_per_loop')))
    buttons.append(types.InlineKeyboardButton(f"📠 Обновить чаты",
                   callback_data=settings_cb.new(action='global_chats')))

    markup.add(*buttons)
    return markup
