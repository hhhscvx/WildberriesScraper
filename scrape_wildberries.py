import asyncio
from http import HTTPStatus

from aiogram.types import InputMediaPhoto, Message
from fake_useragent import UserAgent
from aiohttp import ClientSession

from schemas import Item
from utils import (
    get_basket_version_by_short_id,
    logger,
)


async def scrape_wildberries(
    message: Message,
    http_client: ClientSession,
    artikul: int,
) -> Item:
    """
        Парсит всю инфу по товару артикула.
    """

    part_id = int(artikul / 1000)
    short_id = int(artikul / 100000)
    basket_version = get_basket_version_by_short_id(short_id=short_id)
    url = f"https://basket-{basket_version}.wbbasket.ru/vol{short_id}/part{part_id}/{artikul}/info/ru/card.json"
    logger.info(url)

    response = await http_client.get(url)

    if response.status == HTTPStatus.NOT_FOUND:
        log_message = f"Товар с артикулом {artikul} не найден. Попробуйте ввести еще раз"
        await message.answer(log_message)
        logger.warning(log_message)
        return

    resp_json = await response.json()

    item = Item.model_validate(resp_json)

    logger.success(item.name)
    logger.success(item.category)

    add_data_url = f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&nm={artikul}'
    logger.info(add_data_url)
    add_data_response = await http_client.get(add_data_url)

    add_data = await add_data_response.json()

    try:

        item.photo_count = add_data['data']['products'][0]['pics']
        item.rating = add_data['data']['products'][0]['reviewRating']
        item.reviews_count = add_data['data']['products'][0]['feedbacks']
        item.price = int(add_data['data']['products'][0]['sizes'][0]['price']['product'] / 100)
    except Exception as error:
        log_message = f"Произошла ошибка, скорее всего, товар с артикулом {artikul} не активен. Попробуйте ввести еще раз"
        logger.error(log_message)
        await message.answer(log_message)
        return

    logger.success(f"Photos count: {item.photo_count}")
    logger.success(f"Rating: {item.rating}")
    logger.success(f"Reviews count: {item.reviews_count}")
    logger.success(f"Price: {item.price} руб.")

    item.images_links = [
        f"https://basket-{basket_version}.wbbasket.ru/vol{short_id}/part{part_id}/{artikul}/images/big/{i}.webp;"
        for i in range(1, item.photo_count + 1)]

    item_message = (
        f"Найден товар: <b>{item.name}</b>\n"
        f"Цена: {item.price} руб.\n"
        f"Рейтинг: {item.rating}\n"
    )
    await message.answer(item_message)
    # media = [InputMediaPhoto(media=link) for link in item.images_links]
    # if len(media) > 0:
    #     media[0].caption = item_message
    # if len(media) > 9:
    #     media = media[:8]
    # await message.answer_media_group(media=media)


    return item


async def main():
    """Для тестов"""
    artikul = 27605639
    headers = {'User-Agent': UserAgent().random}
    async with ClientSession(headers=headers) as http_client:
        await scrape_wildberries(http_client=http_client, artikul=artikul)


if __name__ == "__main__":
    asyncio.run(main())
