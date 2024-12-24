import logging
import time

import aiohttp
import os
import uuid

from typing import List, Optional
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile, InputMediaPhoto
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger("aiogram")
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
API_URL = os.getenv("API_URL")

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher()


async def send_process_message(message: types.Message) -> types.Message:
    """
    Отправляет сообщение о процессе.

    :param message: Сообщение от пользователя.
    :return: Ответное сообщение о процессе.
    """
    return await message.reply("⏳ В процессе... ")


async def generate_flowchart(session: aiohttp.ClientSession, algorithm: str, step: int) -> Optional[str]:
    """
    Генерирует блок-схему для алгоритма на заданном шаге.

    :param session: Сессия aiohttp.
    :param algorithm: Алгоритм для генерации схемы.
    :param step: Шаг алгоритма для генерации схемы.
    :return: Путь к файлу с изображением схемы, если успешно, иначе None.
    """
    unique_filename = f"flowchart_{uuid.uuid4().hex}.jpg"
    logger.info(f"Начало запроса для - шаг {step}")

    try:
        async with session.get(API_URL, params={"algorithm": f"{algorithm}"}) as response:
            if response.status == 200:
                logger.info(f"Успешный запрос для - шаг {step}")
                with open(unique_filename, "wb") as file:
                    file.write(await response.read())
                return unique_filename
            else:
                # Логируем статус и тело ответа, если статус не 200
                error_text = await response.text()
                logger.error(f"Ошибка при запросе для - шаг {step}. Статус: {response.status}, Ответ: {error_text}")
    except Exception as e:
        # Логируем исключение, если что-то пошло не так
        logger.exception(f"Исключение при запросе для - шаг {step}: {str(e)}")

    return None


async def send_flowcharts(message: types.Message, temp_files: list[str]) -> None:
    """
    Отправляет несколько блок-схем пользователю.

    :param message: Сообщение от пользователя.
    :param temp_files: Список временных файлов для отправки.
    """
    media_group = [
        InputMediaPhoto(media=FSInputFile(file), caption=f"🎉 Блок-схема {i + 1}")
        for i, file in enumerate(temp_files) if os.path.exists(file)
    ]
    if media_group:
        await message.reply_media_group(media_group)


async def delete_temp_files(temp_files: List[str]) -> None:
    """
    Удаляет временные файлы после их использования.

    :param temp_files: Список временных файлов для удаления.
    """
    for file in temp_files:
        if file and os.path.exists(file):
            os.remove(file)


last_request_time = {}


@dp.message(F.text.startswith("/block"))
async def generate_block(message: types.Message) -> None:
    """
    Обрабатывает команду /block и генерирует блок-схемы для указанного алгоритма.

    :param message: Сообщение от пользователя.
    """
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_request_time and current_time - last_request_time[user_id] < 5:
        await message.reply("❗ Вы слишком часто отправляете запросы. Пожалуйста, подождите немного.")
        return

    last_request_time[user_id] = time.time()

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("❓ Пожалуйста, укажите алгоритм после команды. Пример:\n/block ваш_алгоритм")
        return

    algorithm = args[1]
    temp_files = []
    process_message = await send_process_message(message)

    try:
        async with aiohttp.ClientSession() as session:
            for i in range(3):
                file = await generate_flowchart(session, algorithm, i + 1)
                if file:
                    temp_files.append(file)

        await send_flowcharts(message, temp_files)
        await process_message.delete()

    except Exception:
        await message.reply("Ошибка при генерации схемы. Попробуйте в другой раз...")
    finally:
        await delete_temp_files(temp_files)

    last_request_time[user_id] = time.time()


async def main() -> None:
    """
    Запускает бота.
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
