import json

from aiogram.types import Message
from gspread import service_account

from settings import settings
from utils import logger
from schemas import Item


async def add_or_update_google_sheets(
    message: Message,
    item: Item
) -> None:
    try:
        client = service_account(filename=settings.CREDENTIALS_FILE)
        table = client.open_by_key(settings.SPREADSHEET_ID)

        sheet = table.sheet1

        all_rows = sheet.get_all_records()

        item_data = [
            item.artikul, item.name, item.category,
            item.price, item.description, item.rating,
            item.reviews_count, json.dumps(item.images_links),
            json.dumps(item.specifications, ensure_ascii=False),
        ]
        for idx, row in enumerate(all_rows, start=2):
            if row.get("Артикул") == item.artikul:
                sheet.update(values=[item_data], range_name=f"A{idx}:I{idx}")
                logger.success(f"Обновлена строка {idx} для артикула {item.artikul}.")
                await message.answer(f"Обновлена строка {idx} для артикула {item.artikul}.")
                return

        sheet.append_row(item_data)
        logger.success(f"Добавлена новая строка для артикула {item.artikul}.")
        await message.answer(f"Добавлена новая строка для артикула {item.artikul}.")

    except Exception as error:
        log_message = f"Ошибка при сохранении товара в Google Sheets: {error}"
        logger.error(log_message)
        await message.answer(log_message)


if __name__ == "__main__":
    """Для тестов"""
    add_or_update_google_sheets(23151532, 'futbokla', 5192875)
