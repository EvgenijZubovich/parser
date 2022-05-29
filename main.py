import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram.types import ParseMode
from config import TOKEN, URL
from db import process_search_models, init_db, find_id_search, find_all_merries
from parser import ParserMerries

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='list')
async def send_list(message: types.Message):
    search_models = find_id_search(message.chat.id)
    merries = find_all_merries()
    for merrie in merries:
        merrie_title = merrie.title
        for search_model in search_models:
            seach_title = search_model.title
            if merrie_title.find(seach_title) >= 0:
                message_text = 'Строка поиска {} \r\n Найдено {}'.format(seach_title,
                                                                         utils.markdown.hlink(merrie_title, merrie.url))
                await message.answer(text=message_text, parse_mode=ParseMode.HTML)


@dp.message_handler(commands='search')
async def send_search(message: types.Message):
    search_models = find_id_search(message.chat.id)
    for search_model in search_models:
        await message.answer(text=search_model.title)


@dp.message_handler()
async def echo(message: types.Message):
    await process_search_models(message)


async def scheduled(wait_for, parser):
    while True:
        await asyncio.sleep(wait_for)
        await parser.parse()



if __name__ == '__main__':
    init_db()
    parser = ParserMerries(url=URL, bot=bot)
    lop = asyncio.get_event_loop()
    lop.create_task(scheduled(10, parser))
    executor.start_polling(dp, skip_updates=True)
