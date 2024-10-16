import logging
import asyncio
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.types import InputFile

API_TOKEN = "7486297704:AAHvSrZvD1Bco9gFrgyx6m6v0n5eEokhGzo"

dp = Dispatcher()

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("Виды услуг"),
    KeyboardButton("Контакты"),
    KeyboardButton("Исполнители"),
)

# Категории услуг
services_menu = InlineKeyboardMarkup(row_width=2)
services_menu.add(
    InlineKeyboardButton("Услуга 1", callback_data="service_1"),
    InlineKeyboardButton("Услуга 2", callback_data="service_2"),
    InlineKeyboardButton("Услуга 3", callback_data="service_3"),
    InlineKeyboardButton("Услуга 4", callback_data="service_4"),
    InlineKeyboardButton("Услуга 5", callback_data="service_5"),
)

# Исполнители для услуги
performers = [
    {"name": "Исполнитель 1", "image": "performer_1.jpg"},
    {"name": "Исполнитель 2", "image": "performer_2.jpg"},
    {"name": "Исполнитель 3", "image": "performer_3.jpg"},
    {"name": "Исполнитель 4", "image": "performer_4.jpg"},
    {"name": "Исполнитель 5", "image": "performer_5.jpg"},
]


# Стартовое сообщение
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer(
        "Добро пожаловать в наше агентство!\nВыберите один из разделов:",
        reply_markup=main_menu,
    )


# Виды услуг
@dp.message_handler(lambda message: message.text == "Виды услуг")
async def show_services(message: types.Message):
    await message.answer("Выберите категорию услуг:", reply_markup=services_menu)


# Контакты
@dp.message_handler(lambda message: message.text == "Контакты")
async def show_contacts(message: types.Message):
    await message.answer("Наши контакты:\nТелефон: +123456789\nEmail: info@agency.com")


# Исполнители
@dp.message_handler(lambda message: message.text == "Исполнители")
async def show_all_performers(message: types.Message):
    await message.answer("Наши исполнители:")
    for performer in performers:
        photo = InputFile(performer["image"])
        await message.answer_photo(
            message.chat.id, photo=photo, caption=performer["name"]
        )


# Обработка кликов по услугам
@dp.callback_query_handler(lambda c: c.data.startswith("service_"))
async def show_performers_for_service(callback_query: types.CallbackQuery):
    service_id = callback_query.data.split("_")[1]
    await callback_query.answer_callback_query(callback_query.id)
    await callback_query.answer(
        callback_query.from_user.id, f"Исполнители для услуги {service_id}:"
    )
    for performer in performers:
        photo = InputFile(performer["image"])
        await callback_query.answer_photo(
            callback_query.from_user.id, photo=photo, caption=performer["name"]
        )


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=API_TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


# Запуск бота
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
