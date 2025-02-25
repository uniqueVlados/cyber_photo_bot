# -*- coding: utf-8 -*-

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import shutil
from dotenv import load_dotenv

import os

from db import Db

load_dotenv()

API_TOKEN = "6127934377:AAH4cZn1sXhbS63BhCBmHuQFs-oJ6J7wqZI" #str(os.getenv('TOKEN'))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db_client = Db("users.db")

# BUTTONS
SHEDULE_BTN = KeyboardButton('Расписание📅')
RATING_BTN = KeyboardButton('Рейтинг📉')
TIME_YES_BTN = KeyboardButton('ДА ✅')
TIME_NO_BTN = KeyboardButton('НЕТ ❌')

# KEYBOARDS
MAIN_KB = ReplyKeyboardMarkup(resize_keyboard=True)
MAIN_KB.add(SHEDULE_BTN, RATING_BTN)
TIME_KB = ReplyKeyboardMarkup(resize_keyboard=True)
TIME_KB.add(TIME_YES_BTN, TIME_NO_BTN)

# CONST
FONT_PATH = "resources/fonts/main.ttf"


def create_shedule_photo(user_id, tour, div, game, commands):
    shedule_time = db_client.get_last_time_user(user_id)
    font_time = ImageFont.truetype(font=FONT_PATH, size=15)
    if shedule_time:
        day = db_client.get_last_time_user(user_id).split()[0].lower()
        time = "   " + db_client.get_last_time_user(user_id).split()[1].lower()

    base = Image.open("img/shedule_main.png")
    game_p = Image.open(f"img/{game}.png").convert('RGBA').resize((140, 140))
    div_p = Image.open(f"img/{div}.png").convert('RGBA').resize((140, 140))
    base.paste(game_p, (852, 70), game_p)
    base.paste(div_p, (1060, 73), div_p)

    tour_text = tour
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(font=FONT_PATH, size=34)
    text_color = (255, 255, 255)
    draw.text((32, 43), tour_text, font=font, fill=text_color)

    font = ImageFont.truetype(font=FONT_PATH, size=18)

    x = 120
    y = 265
    for item in commands[:8]:
        draw.text((x, y), item[0], font=font, fill=text_color)
        if shedule_time:
            draw.text((x + 235, y - 9), day, font=font_time, fill=text_color)
            draw.text((x + 235, y + 11), time, font=font_time, fill=text_color)
        draw.text((x + 328, y), item[1], font=font, fill=text_color)
        y += 54

    if len(commands) > 8:
        x = 702
        y = 268
        for item in commands[8:16]:
            draw.text((x, y), item[0], font=font, fill=text_color)
            if shedule_time:
                draw.text((x + 235, y - 7), day, font=font_time, fill=text_color)
                draw.text((x + 235, y + 11), time, font=font_time, fill=text_color)
            draw.text((x + 328, y), item[1], font=font, fill=text_color)
            y += 54

    base.save(f"user_files/{user_id}/shedule/shedule_1.png")

    count_img = (len(commands) - 16) // 16 + 1
    first = 16
    for i in range(2, count_img + 2):
        base = Image.open("img/shedule.png")
        draw = ImageDraw.Draw(base)
        text_color = (255, 255, 255)
        font = ImageFont.truetype(font=FONT_PATH, size=34)
        draw.text((32, 43), tour_text, font=font, fill=text_color)
        font = ImageFont.truetype(font=FONT_PATH, size=18)
        x = 112
        y = 154
        for item in commands[first:first + 8]:
            draw.text((x, y), str(item[0]), font=font, fill=text_color)
            if shedule_time:
                draw.text((x + 235, y - 7), day, font=font_time, fill=text_color)
                draw.text((x + 235, y + 11), time, font=font_time, fill=text_color)
            draw.text((x + 320, y), str(item[1]), font=font, fill=text_color)
            y += 54
        first += 8
        x = 700
        y = 154
        for item in commands[first:first + 8]:
            draw.text((x, y), str(item[0]), font=font, fill=text_color)
            if shedule_time:
                draw.text((x + 235, y - 7), day, font=font_time, fill=text_color)
                draw.text((x + 235, y + 11), time, font=font_time, fill=text_color)
            draw.text((x + 320, y), str(item[1]), font=font, fill=text_color)
            y += 54
        first += 8
        base.save(f"user_files/{user_id}/shedule/shedule_{i}.png")


def create_rating_photo(user_id, tour, div, game, commands):
    base = Image.open("img/rating_main.png")
    game_p = Image.open(f"img/{game}.png").convert('RGBA').resize((140, 140))
    div_p = Image.open(f"img/{div}.png").convert('RGBA').resize((140, 140))
    base.paste(game_p, (852, 70), game_p)
    base.paste(div_p, (1060, 73), div_p)

    tour_text = tour
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(font=FONT_PATH, size=34)
    text_color = (255, 255, 255)
    draw.text((32, 43), tour_text, font=font, fill=text_color)

    font = ImageFont.truetype(font=FONT_PATH, size=20)

    x = 165
    y = 305
    count = 1
    for item in commands[:6]:
        draw.text((x, y), str(count), font=font, fill=text_color)
        draw.text((x + 59, y), str(item[0]), font=font, fill=text_color)
        draw.text((x + 390, y), str(item[1]), font=font, fill=text_color)
        y += 65
        count += 1

    x = 685
    y = 305
    for item in commands[6:12]:
        draw.text((x, y), str(count), font=font, fill=text_color)
        draw.text((x + 59, y), str(item[0]), font=font, fill=text_color)
        draw.text((x + 390, y), str(item[1]), font=font, fill=text_color)
        y += 65
        count += 1

    base.save(f"user_files/{user_id}/rating/rating_1.png")

    count_img = (len(commands) - 12) // 16 + 1
    first = 12
    for i in range(2, count_img + 2):
        base = Image.open("img/rating.png")
        draw = ImageDraw.Draw(base)
        text_color = (255, 255, 255)
        font = ImageFont.truetype(font=FONT_PATH, size=34)
        draw.text((32, 43), tour_text, font=font, fill=text_color)
        font = ImageFont.truetype(font=FONT_PATH, size=22)
        x = 172
        y = 125
        for item in commands[first:first + 8]:
            draw.text((x, y), str(count), font=font, fill=text_color)
            draw.text((x + 59, y), str(item[0]), font=font, fill=text_color)
            draw.text((x + 393, y), str(item[1]), font=font, fill=text_color)
            y += 65
            count += 1
        first += 8
        x = 695
        y = 125
        for item in commands[first:first + 8]:
            draw.text((x, y), str(count), font=font, fill=text_color)
            draw.text((x + 59, y), str(item[0]), font=font, fill=text_color)
            draw.text((x + 395, y), str(item[1]), font=font, fill=text_color)
            y += 65
            count += 1
        first += 8
        base.save(f"user_files/{user_id}/rating/rating_{i}.png")


def generate_shedule(file, user_id):
    matrix = file.to_numpy()
    tour, div, game = matrix[0][0], matrix[0][1], matrix[0][2]
    commands = [(item[1], item[2]) for item in matrix[1:]]
    create_shedule_photo(user_id, tour, div, game, commands)


def generate_rating(file, user_id):
    matrix = file.to_numpy()
    tour, div, game = matrix[0][1], matrix[0][2], matrix[0][3]
    commands = [(item[1], item[2]) for item in matrix[3:]]
    create_rating_photo(user_id, tour, div, game, commands)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = int(message.from_user.id)
    os.makedirs(f'user_files/{user_id}', exist_ok=True)
    os.makedirs(f'user_files/{user_id}/shedule', exist_ok=True)
    os.makedirs(f'user_files/{user_id}/rating', exist_ok=True)
    state = "start"
    if db_client.check_user(user_id):
        db_client.set_state_user(user_id, state)
    else:
        db_client.add_user(user_id, state)
    await message.reply(
        f"Привет, {message.from_user.first_name}\n\nТеперь ты можешь не еб*ться в Figma и"
        f" быстро составлять расписание и рейтинг по своей таблице.\n😎You are welcome😎\n"
        f"🔻Выбери, что тебе сейчас необходимо🔻",
        reply_markup=MAIN_KB)


@dp.message_handler()
async def btn_check(message: types.Message):
    user_id = int(message.from_user.id)
    if message.text == 'Расписание📅' and db_client.get_state_user(user_id) == "start":
        db_client.set_state_user(user_id, "shedule_time")
        await message.reply("Хочешь проставить время для матчей❓\n©У всех пар оно будет одинаковым.",
                            reply_markup=TIME_KB)

    elif db_client.get_state_user(user_id) == "shedule_time_input":
        db_client.set_last_time_user(user_id, message.text)
        db_client.set_state_user(user_id, "shedule")
        await message.reply(
            f"Запомнил✅\n\n"
            f"Отправь мне файл с таблицей (один лист)\n"
            f"⬇Написать в таблице можно лишь эти данные в нужных ячейках⬇\n\n"
            f"🔴Дивизионы: small/middle/college\n\n"
            f"🔴Дисциплины: caliber/chess/cs/dota/fallguys/fifa/fortnite/lol/mlbb/pubg/standoff/valorant/tanks\n\n"
            f"Вот пример👇",
            reply_markup=ReplyKeyboardRemove())
        with open("resources/shedule.xlsx", 'rb') as f:
            await bot.send_document(user_id, document=f)
    elif message.text == 'ДА ✅' and db_client.get_state_user(user_id) == "shedule_time":
        db_client.set_state_user(user_id, "shedule_time_input")
        await message.reply("Введи время в формате\n\n➡   day hh:mm   ⬅\n\n☑Пример: среда 17:00",
                            reply_markup=ReplyKeyboardRemove())

    elif message.text == 'НЕТ ❌' and db_client.get_state_user(user_id) == "shedule_time":
        db_client.set_last_time_user(user_id, None)
        db_client.set_state_user(user_id, "shedule")
        await message.reply(
            f"Отправь мне файл с таблицей (один лист)\n"
            f"⬇Написать в таблице можно лишь эти данные в нужных ячейках⬇\n\n"
            f"🔴Дивизионы: small/middle/college\n\n"
            f"🔴Дисциплины: caliber/chess/cs/dota/fallguys/fifa/fortnite/lol/mlbb/pubg/standoff/valorant\n\n"
            f"Вот пример👇",
            reply_markup=ReplyKeyboardRemove())
        with open("resources/shedule.xlsx", 'rb') as f:
            await bot.send_document(user_id, document=f)

    elif message.text == 'Рейтинг📉' and db_client.get_state_user(user_id) == "start":
        db_client.set_state_user(user_id, "rating")
        await message.reply(
            f"Отправь мне файл с таблицей (один лист)\n"
            f"⬇Написать в таблице можно лишь эти данные в нужных ячейках⬇\n\n"
            f"🔴Дивизионы: small/middle/college\n\n"
            f"🔴Дисциплины: caliber/chess/cs/dota/fallguys/fifa/fortnite/lol/mlbb/pubg/standoff/valorant\n\n"
            f"Вот пример👇",
            reply_markup=ReplyKeyboardRemove())
        with open("resources/rating.xlsx", 'rb') as f:
            await bot.send_document(user_id, document=f)


@dp.message_handler(content_types=['document'])
async def handle_docs_photo(message: types.Message):
    user_id = int(message.from_user.id)
    document = message.document
    file_id = document.file_id
    file_info = await bot.get_file(file_id)
    path_to_file = file_info.file_path

    if db_client.get_state_user(user_id) == "shedule":
        path = f'user_files/{user_id}/shedule.xlsx'
    elif db_client.get_state_user(user_id) == "rating":
        path = f'user_files/{user_id}/rating.xlsx'

    await bot.download_file(path_to_file, destination=path)
    file = pd.read_excel(path)

    if db_client.get_state_user(user_id) == "shedule":
        generate_shedule(file, user_id)
        for file in os.listdir(f"user_files/{user_id}/shedule"):
            with open(f"user_files/{user_id}/shedule/{file}", 'rb') as photo:
                await bot.send_photo(chat_id=user_id, photo=photo)
        shutil.rmtree(f"user_files/{user_id}/shedule")

    elif db_client.get_state_user(user_id) == "rating":
        generate_rating(file, user_id)
        for file in os.listdir(f"user_files/{user_id}/rating"):
            with open(f"user_files/{user_id}/rating/{file}", 'rb') as photo:
                await bot.send_photo(chat_id=user_id, photo=photo)
        shutil.rmtree(f"user_files/{user_id}/rating")

    db_client.set_state_user(user_id, "start")
    await message.reply(
        f"Вуаля.\nЕсли что-то не так - введи команду\n/start",
        reply_markup=MAIN_KB)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
