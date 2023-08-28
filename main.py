import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from voice_converter import VoiceConverter

TELEBOT_TOKEN = '6375255466:AAH6xHuo8QoiDJttiVpPasNcxKMax1mgOis'
TELEBOT_REPO = 'https://github.com/imasloff/yandex_test_bot'

bot = Bot(TELEBOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    name = message.chat.full_name if message.chat.full_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.chat.id}) started bot")

    markup = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    keyboard = [
        types.KeyboardButton('Селфи'),
        types.KeyboardButton('Фото из старшей школы'),
        types.KeyboardButton('Хобби'),
        types.KeyboardButton('Получить войс'),
    ]
    markup.add(*keyboard)
    await message.answer(f'Привет, {name}!', reply_markup=markup)


@dp.message_handler(commands=['repo'])
async def repo(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Перейти в репозиторий', url=TELEBOT_REPO)
    markup.add(btn)
    await message.answer('Нажмите кнопку', reply_markup=markup)


@dp.message_handler(commands=['help', 'info'])
async def info(message: types.Message):
    await message.answer('Функционал:\n/start - начать общение с ботом\n/repo - перейти в репозиторий бота\n\nТакже боту можно давать команды кнопками и текстом (но не факт, что он вас поймет).')


@dp.message_handler(content_types=['audio', 'voice'])
async def get_voice_command(message: types.Message):
    try:
        file_id = message.voice.file_id
        downloaded_file = await bot.download_file_by_id(file_id)
        filename = str(message.message_id) + '.ogg'

        name = message.chat.full_name if message.chat.full_name else 'No_name'
        logger.info(
            f"Chat {name} (ID: {message.chat.id}) download file {filename}")

        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file.read())
        converter = VoiceConverter(filename)
        os.remove(filename)
        command_text = converter.audio2text().lower()
        del converter
    except Exception as e:
        await message.answer('Не получилось расшифровать голосовое :(')
        name = message.chat.full_name if message.chat.full_name else 'No_name'
        logger.exception(
            f"Chat {name} (ID: {message.chat.id}) Exception while recognizing speech: {e}")

    if 'селф' in command_text:
        await message.answer(
            f'Я понял, что Вы сказали:\n"{command_text}".\n\nНажмите "Селфи" на клавиатуре')
    elif ('школ' or 'фото') in command_text:
        await message.answer(
            f'Я понял, что Вы сказали:\n"{command_text}".\n\nНажмите "Фото из старшей школы" на клавиатуре')
    elif any(sub in command_text for sub in ('хобби', 'увлечен')):
        await message.answer(
            f'Я понял, что Вы сказали:\n"{command_text}".\n\nНажмите "Хобби" на клавиатуре')
    elif any(sub in command_text for sub in ('войс', 'голос', 'аудио')):
        await message.answer(
            f'Я понял, что Вы сказали:\n"{command_text}".\n\nНажмите "Получить войс" на клавиатуре')
    else:
        await message.answer(
            f'Я понял, что Вы сказали:\n"{command_text}".\n\nК сожалению, не знаю такой команды, воспользуйтесь клавиатурой.')


@dp.message_handler(lambda message: 'селф' in message.text.lower())
async def selfie(message: types.Message):
    filename = 'images/selfie.jpg'
    selfie = open(filename, 'rb')
    await message.answer_photo(selfie, 'Полюбуйтесь на меня!')


@dp.message_handler(lambda message: ('школ' or 'фото') in message.text.lower())
async def high_school_photo(message: types.Message):
    filename = 'images/high_school_photo.jpg'
    hs_photo = open(filename, 'rb')
    await message.answer_photo(hs_photo, 'Полюбуйтесь на меня, школьника!')


@dp.message_handler(lambda message: any(sub in message.text.lower() for sub in ('хобби', 'увлечен')))
async def hobby(message: types.Message):
    await message.answer(
        '<strong>Музыка и геймдизайн</strong> - мои главные увлечения, помимо AI.\n<u>Музыка</u> - мое основное хобби с самого детства, я играю на гитаре и фортепиано, а также пою. До этого года пел басом в студенческом хоре.\n<u>Геймдизайн</u> - это хобби появилось у меня не так давно, хотя страсть к играм я питаю с детства. Теперь процесс написания ГДД мне приносит не меньше удовольствия, чем прохождение новых игр.',
        parse_mode=types.ParseMode.HTML
    )


@dp.message_handler(lambda message: any(sub in (message.text.lower() or message) for sub in ('войс', 'голос', 'аудио')))
async def send_voice(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard = [
        types.InlineKeyboardButton('Объясни GPT', callback_data='gpt'),
        types.InlineKeyboardButton('Объясни SQL/noSQL', callback_data='sql'),
        types.InlineKeyboardButton(
            'Расскажи про первую любовь', callback_data='first_love'),
    ]
    markup.add(*keyboard)
    await message.answer('Выберите голосовое', reply_markup=markup)


@dp.callback_query_handler(lambda call: True)
async def callback(call: types.CallbackQuery):
    prefix = 'voices/'
    postfix = '.ogg'
    voice = open(prefix + call.data + postfix, 'rb')
    await call.message.answer_voice(voice, f'Послушайте войс про {call.data}')

if __name__ == '__main__':
    logger.info("Starting bot")
    executor.start_polling(dp)
