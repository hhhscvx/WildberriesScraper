import json
import requests

from fake_useragent import UserAgent

from schemas import Item
from utils import (
    get_basket_version_by_short_id,
    logger,
)


def scrape_wildberries(artikul: int) -> Item:
    """
        Парсит всю инфу по товару артикула.
    """

    part_id = int(artikul / 1000)
    short_id = int(artikul / 100000)
    basket_version = get_basket_version_by_short_id(short_id=short_id)
    url = f"https://basket-{basket_version}.wbbasket.ru/vol{short_id}/part{part_id}/{artikul}/info/ru/card.json"
    logger.info(url)

    headers = {'User-Agent': UserAgent().random}
    data = requests.get(url, headers=headers)

    print(data.text)

    item = json.loads(data.text)

    item = Item.model_validate(item)

    logger.success(item.name)
    logger.success(item.category)

    add_data_url = f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&nm={artikul}'
    logger.info(add_data_url)
    add_data = requests.get(add_data_url, headers=headers)

    add_data = json.loads(add_data.text)

    item.photo_count = add_data['data']['products'][0]['pics']
    item.rating = add_data['data']['products'][0]['reviewRating']
    item.reviews_count = add_data['data']['products'][0]['feedbacks']
    item.price = int(add_data['data']['products'][0]['sizes'][0]['price']['product'] / 100)

    logger.success(f"Photos count: {item.photo_count}")
    logger.success(f"Rating: {item.rating}")
    logger.success(f"Reviews count: {item.reviews_count}")
    logger.success(f"Price: {item.price} руб.")



if __name__ == "__main__":
    artikul = 27605639
    scrape_wildberries(artikul=artikul)
