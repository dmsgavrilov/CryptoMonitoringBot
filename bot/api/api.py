import logging

from asyncio import get_event_loop

from aiogram import executor, types
from aiogram.dispatcher import filters

from bot import utils
from bot.api.bot_init import db, dp, bot
from bot.config import settings

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    utils.get_user(db, message.chat.id)
    await bot.send_message(
        message.chat.id, 'Привет, я КриптоБот\n'
        'Со мной ты всегда будешь в курсе всего, что происходит на бирже криптовалют'
    )
    await bot.send_message(
        message.chat.id,
        'Для общения со мной используй комманды:\n\n'
        '/add <strong>currencies</strong> - добавить отслеживаемые валюты\n\n'
        '/delete <strong>currencies</strong> - удалить отслеживаемые валюты\n\n'
        '/get_currencies - посмотреть список отслеживаемых валют\n\n'
        '/stop_monitoring - прекратить отслеживание\n\n'
    )
    await bot.send_message(
        message.chat.id,
        f'Список отслеживаемых валют можно посмотреть на сайте: {settings.CURRENCY_URL}'
    )


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['add [A-Za-z ]+']))
async def add_currencies(message: types.Message, regexp_command):
    titles = regexp_command.group(0).replace('add ', '').split()
    utils.add_currencies(db, message.chat.id, titles)
    await bot.send_message(
        message.chat.id,
        'Выбранные валюты теперь отслеживаются'
    )


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['delete [A-Za-z ]+']))
async def delete_currencies(message: types.Message, regexp_command):
    titles = regexp_command.group(0).replace('delete ', '').split()
    utils.delete_currencies(db, message.chat.id, titles)
    await bot.send_message(
        message.chat.id,
        'Выбранные валюты больше не отслеживаются'
    )


@dp.message_handler(commands=['get_currencies'])
async def get_currencies(message: types.Message):
    currencies = utils.get_currencies(db, message.chat.id)
    if currencies == []:
        message_text = 'Пока ничего не отслеживается'
    else:
        message_text = f'Отсеживаемые валюты:\n'
        for currency in currencies:
            message_text += f'{currency.title} - {currency.rate}$\n'
    await bot.send_message(
        message.chat.id,
        message_text
    )


@dp.message_handler(commands=['stop_monitoring'])
async def stop_monitoring(message: types.Message):
    utils.delete_all_currencies(db, message.chat.id)
    await bot.send_message(
        message.chat.id,
        'Отслеживание прекращено'
    )


if __name__ == '__main__':
    loop = get_event_loop()
    loop.create_task(utils.update_rates(db, 3))
    executor.start_polling(dp, skip_updates=True)
