import asyncio
import json

from fake_useragent import UserAgent
from aiohttp import ClientSession

from schemas import Item
from utils import (
    get_basket_version_by_short_id,
    logger,
)


async def scrape_wildberries(http_client: ClientSession, artikul: int) -> Item:
    """
        Парсит всю инфу по товару артикула.
    """

    part_id = int(artikul / 1000)
    short_id = int(artikul / 100000)
    basket_version = get_basket_version_by_short_id(short_id=short_id)
    url = f"https://basket-{basket_version}.wbbasket.ru/vol{short_id}/part{part_id}/{artikul}/info/ru/card.json"
    logger.info(url)

    response = await http_client.get(url)

    resp_json = await response.json()

    item = Item.model_validate(resp_json)

    logger.success(item.name)
    logger.success(item.category)

    add_data_url = f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&nm={artikul}'
    logger.info(add_data_url)
    add_data_response = await http_client.get(add_data_url)

    add_data = await add_data_response.json()

    item.photo_count = add_data['data']['products'][0]['pics']
    item.rating = add_data['data']['products'][0]['reviewRating']
    item.reviews_count = add_data['data']['products'][0]['feedbacks']
    item.price = int(add_data['data']['products'][0]['sizes'][0]['price']['product'] / 100)

    logger.success(f"Photos count: {item.photo_count}")
    logger.success(f"Rating: {item.rating}")
    logger.success(f"Reviews count: {item.reviews_count}")
    logger.success(f"Price: {item.price} руб.")

    item.images_links = [
        f"https://basket-{basket_version}.wbbasket.ru/vol{short_id}/part{part_id}/{artikul}/images/big/{i}.webp;"
        for i in range(1, item.photo_count + 1)]



async def main():
    artikul = 27605639
    headers = {'User-Agent': UserAgent().random}
    async with ClientSession(headers=headers) as http_client:
        await scrape_wildberries(http_client=http_client, artikul=artikul)


if __name__ == "__main__":
    asyncio.run(main())
