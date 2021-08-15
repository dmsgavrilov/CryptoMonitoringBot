import logging

from aiogram import Bot, Dispatcher, executor, types

from bot.config import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await bot.send_message(
        message.chat.id, 'Привет, я КриптоБот\n'
        'Со мной ты всегда будешь в курсе всего, что происходит на бирже криптовалют'
    )
    await bot.send_message(
        message.chat.id, 'Для общения со мной используй комманды:\n\n'
                         '/set_currencies - чтобы задать список отслеживаемых валют\n\n'
                         '/change_currencies - чтобы изменить список отслеживаемых валют '
    )


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
