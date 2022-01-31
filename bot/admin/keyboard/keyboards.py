from aiogram import types


def admin_keyboard():
    """Стартовая клавиатура для админов"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name)
                 for name in ['☎ Клиенты', '🐝 Модеры']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['📄 Сессии']])
    keyboard.add(*[types.KeyboardButton(name)
                 for name in ['♻ Настройки', '📜 Отчёты', "📳 Оповещения"]])
    keyboard.add(*[types.KeyboardButton(name)
                 for name in ['📜 На модерации', 'Подготовка сессий']])
    return keyboard
