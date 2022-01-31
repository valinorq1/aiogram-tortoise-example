from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext

from admin.models import GlobalSettings, StaticText, Channels
from bot_config import dp, bot
from admin.keyboard.settings_inline import get_settings_inline


class EditGlobalMessageIntervalState(StatesGroup):
    new_message_interval = State()


@dp.message_handler(state=EditGlobalMessageIntervalState.new_message_interval)
async def change_msg_global_interval(m: types.Message, state: FSMContext):
    """send new global message interval"""
    try:
        if m.text.split("-")[0].isdigit() and m.text.split("-")[1].isdigit():
            await GlobalSettings.first().update(
                message_interval_min=m.text.split("-")[0],
                message_interval_max=m.text.split("-")[1]
            )

            await bot.send_message(
                m.chat.id,
                f'Успешно изменили глобальный интервал между сообщениями',
                reply_markup=await get_settings_inline(),
            )
        else:
            await bot.send_message(m.chat.id, f"Ошибка, возможно вы указали интервал в неправильном формате.")
            await state.finish()
            return
    except:
        await bot.send_message(m.chat.id, f"Произошла ошибка")
    finally:
        await state.finish()


class EditGlobalLoopIntervalState(StatesGroup):
    new_loop_interval = State()


@dp.message_handler(state=EditGlobalLoopIntervalState.new_loop_interval)
async def change_loop_global_interval(m: types.Message, state: FSMContext):
    """set new global interval for loop"""
    try:
        if m.text.split("-")[0].isdigit() and m.text.split("-")[1].isdigit():
            await GlobalSettings.first().update(
                loop_interval_min=m.text.split("-")[0],
                loop_interval_max=m.text.split("-")[1])
            await bot.send_message(
                m.chat.id,
                f'Успешно изменили глобальный цикловый интервал',
                reply_markup=await get_settings_inline(),
            )
            await state.finish()
            return
        else:
            await bot.send_message(m.chat.id, f"Ошибка, возможно вы указали интервал в неправильном формате.")
            await state.finish()
            return
    except:
        await bot.send_message(m.chat.id, f"Произошла ошибка")
    finally:
        await state.finish()


class UpdateWelcomeText(StatesGroup):
    new_text = State()


@dp.message_handler(state=UpdateWelcomeText.new_text)
async def set_welcome_text(m: types.Message, state: FSMContext):
    """set new text for /start command"""
    try:
        await StaticText.first().update(welcome=m.text)
        await bot.send_message(
            m.chat.id,
            f'Успешно обновили текст привествия.',
            reply_markup=await get_settings_inline(),
        )
    except Exception as e:
        print(e)
        await bot.send_message(m.chat.id, 'Произошла ошибка.')
    finally:
        await state.finish()


class UpdateSupportText(StatesGroup):
    new_text = State()


@dp.message_handler(state=UpdateSupportText.new_text)
async def set_rules_new_text(m: types.Message, state: FSMContext):
    """set new text for rules button"""
    try:
        await StaticText.first().update(support=m.text)
        await bot.send_message(
            m.chat.id,
            f'Успешно обновили текст для кнопки СВЯЗЬ С ПОДДЕРЖКОЙ.',
            reply_markup=await get_settings_inline(),
        )
    except Exception as e:
        print(e)
        await bot.send_message(m.chat.id, 'Произошла ошибка.')
    finally:
        await state.finish()


class UpdateRulesText(StatesGroup):
    new_text = State()


@dp.message_handler(state=UpdateRulesText.new_text)
async def set_support_new_text(m: types.Message, state: FSMContext):
    """set new text for support button"""
    try:
        await StaticText.first().update(rules=m.text)
        await bot.send_message(
            m.chat.id,
            f'Успешно обновили текст для кнопки ПРАВИЛА.',
            reply_markup=await get_settings_inline(),
        )
    except Exception as e:
        print(e)
        await bot.send_message(m.chat.id, 'Произошла ошибка.')
    finally:
        await state.finish()


class UpdateLoopMessageLimit(StatesGroup):
    new_limit = State()


@dp.message_handler(state=UpdateLoopMessageLimit.new_limit)
async def set_new_loop_limit(m: types.Message, state: FSMContext):
    """set new message limit per loop"""
    try:
        await GlobalSettings.first().update(message_limit=int(m.text))
        await bot.send_message(
            m.chat.id,
            f'Успешно обновили лимит.',
            reply_markup=await get_settings_inline(),
        )
    except:
        await bot.send_message(m.chat.id, "Лимит должен быть указан в цифрах")

    finally:
        await state.finish()


class UpdateChatsList(StatesGroup):
    new_chat_file = State()


@dp.message_handler(content_types=["document"], state=UpdateChatsList.new_chat_file)
async def update_global_chats_list(m: types.Message, state: FSMContext):
    try:
        file = await bot.get_file(m.document.file_id)
        await bot.download_file(file.file_path, f"static/chats.csv")
        with open("static/chats.csv", "r") as fh:
            chats = fh.read()
        new_data = chats.split("\n")
        for i in new_data:
            if i:
                i = i.split(",")
                await Channels.update_or_create(channel=i[0].replace("\"", ""), defaults=dict(timeout=int(i[1])))
        await bot.send_message(
            m.chat.id,
            f'Успешно обновили файл с чатами.',
            reply_markup=await get_settings_inline(),
        )
    except Exception as e:
        print(e)
        await bot.send_message(m.chat.id, 'При обработке файла произошла ошибка, '
                                          'проверьте файл еще раз и попробуйте снова.')
    finally:
        await state.finish()
