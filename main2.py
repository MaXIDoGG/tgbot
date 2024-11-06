import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.types import FSInputFile

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Виды услуг"),
            KeyboardButton(text="Контакты"),
            KeyboardButton(text="Исполнители"),
        ]
    ],
    resize_keyboard=True,
)

# Категории услуг
services_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Услуга 1", callback_data="service_1"),
            InlineKeyboardButton(text="Услуга 2", callback_data="service_2"),
            InlineKeyboardButton(text="Услуга 3", callback_data="service_3"),
            InlineKeyboardButton(text="Услуга 4", callback_data="service_4"),
            InlineKeyboardButton(text="Услуга 5", callback_data="service_5"),
        ]
    ],
    row_width=2,
)

# Исполнители для услуги
performers = [
    {"name": "Исполнитель 1", "image": "performer_1.jpg"},
    {"name": "Исполнитель 2", "image": "performer_1.jpg"},
    {"name": "Исполнитель 3", "image": "performer_1.jpg"},
    {"name": "Исполнитель 4", "image": "performer_1.jpg"},
    {"name": "Исполнитель 5", "image": "performer_1.jpg"},
]


# Стартовое сообщение
@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer(
        "Добро пожаловать в наше агентство!\nВыберите один из разделов:",
        reply_markup=main_menu,
    )


# Виды услуг
@dp.message(lambda message: message.text == "Виды услуг")
async def show_services(message: Message):
    await message.answer("Выберите категорию услуг:", reply_markup=services_menu)


# Контакты
@dp.message(lambda message: message.text == "Контакты")
async def show_contacts(message: Message):
    await message.answer("Наши контакты:\nТелефон: +123456789\nEmail: info@agency.com")


# Исполнители
@dp.message(lambda message: message.text == "Исполнители")
async def show_all_performers(message: Message):
    await message.answer("Наши исполнители:")
    for performer in performers:
        photo = FSInputFile("img/" + performer["image"])
        await message.answer_photo(photo=photo, caption=performer["name"])


# Обработка кликов по услугам
@dp.callback_query(lambda c: c.data.startswith("service_"))
async def show_performers_for_service(callback_query: types.CallbackQuery):
    service_id = callback_query.data.split("_")[1]
    # await callback_query.answer_callback_query(callback_query.id)
    await callback_query.message.answer(text=f"Исполнители для услуги {service_id}:")
    for performer in performers:
        photo = FSInputFile("img/" + performer["image"])
        await callback_query.message.answer_photo(
            photo=photo, caption=performer["name"]
        )


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
