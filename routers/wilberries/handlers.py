import asyncio
from functools import partial

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from fake_useragent import UserAgent

from scrape_wildberries import scrape_wildberries
from .state import WBItem
from utils import add_or_update_google_sheets


router = Router(name=__name__)


@router.message(CommandStart())
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Введите артикул товара")
    await state.set_state(WBItem.artikul)


@router.message(WBItem.artikul, lambda msg: msg.text.isdigit())
async def item_artikul_handler(message: Message, state: FSMContext):
    artikul = int(message.text)
    headers = {'User-Agent': UserAgent().random}
    async with ClientSession(headers=headers) as http_client:
        item = await scrape_wildberries(http_client=http_client, artikul=artikul)

    await asyncio.to_thread(partial(add_or_update_google_sheets, item))
