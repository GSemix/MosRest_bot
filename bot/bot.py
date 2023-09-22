#!/usr/bin/python3
# -*- coding: utf-8 -*-

from re import findall
from os import remove
from os import listdir
from os import path
from os.path import isfile
from os.path import isdir
from sys import argv
from json import loads

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage # Хранилище состояний
from aiogram.utils.executor import start_webhook
import asyncio

from config_reader import config
from messages import *
from file import *
from other import *
from templates import *
from logger import logger
from db import BD
from db import params
from check_logs import last24HourUsersActivity
from check_logs import lastWeekUsersActivity

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Состояния:
#   main
#	doc_users
#   location

"""         <WEBHOOK>"""
# webhook settings
WEBHOOK_HOST = 'https://digitalplatforms.su'
WEBHOOK_PATH = '/new_mos_rest_bot'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3005

itude_zone = 0.02
itude_zone_max = 0.2

# Объект бота
bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="html")
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())
# База данных
bd = BD(params)

# Команды

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    logger.info(getLogWithUsersId(id, '=', "Pressed '/start'"))

    try:
        user = await bd.getUserById(id)

        if user == None:
            user = t_user()
            user['id'] = id
            user['username'] = username
            await setUser(user, bd)
            logger.info(getLogWithUsersId(id, '+', "Append new user"))
        else:
            if await isAccess(id, bd):
                user["username"] = username
                user["state"] = "main"
                await updateUser(user, bd)
                logger.info(getLogWithUsersId(id, '+', "Info about user updated"))

    except Exception as e:
        await errorMessage(bot, message, e)
        logger.error(getLogWithUsersId(id, '-', f"Error in 'cmd_start': {e}"))

    if await isAccess(id, bd):
        telegram_id = await bd.get_sticker_by_name_and_family("start", "main")

        if telegram_id:
            await getCmdStickerMessage(bot, message, telegram_id)
        await getCmdStartMessage(bot, message)
    else:
        await blockMessage(bot, message)
        logger.warning(getLogWithUsersId(id, '?', "Detected user without ACCESS"))

@dp.message_handler(commands=["parameters"])
async def cmd_parameters(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/parameters'"))

        try:
            await getCmdParametersMessage(bot, message)
            await setState(id, 'parameters', bd)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'cmd_parameters': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["search"])
async def cmd_search(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/search'"))

        try:
            await getCmdSearchMessage(bot, message)
            await setState(id, 'search', bd)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'cmd_search': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["favorites"])
async def cmd_favorites(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/favorites'"))

        try:
            await getCmdFavoritesMessage(bot, message)
            await setState(id, 'main', bd)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'cmd_favorites': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["random"])
async def cmd_random(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/random'"))

        try:
            rest = await bd.getRandomRestaurant()
            if rest != None:
                reviews = await bd.getRestaurantsReviewsByRestId(rest["id"])
                promotions = await bd.getRestaurantsPromotionsByRestId(rest["id"])
                #telegram_id = await bd.get_sticker_by_name_and_family("random", "main")

                #if telegram_id:
                    #stickers_message = await getCmdStickerMessage(bot, message, telegram_id)
                    #print(stickers_message)
                    #await asyncio.sleep(1)
                    #await bot.delete_message(chat_id=message.from_user.id, message_id=stickers_message.message_id)

                await getRestaurantsMessage(bot, id, rest, promotions)

                if reviews:
                    await getRestaurantsReviewsMessage(bot, id, reviews)
            else:
                await getGooseMessage(bot, id)

            await setState(id, 'main', bd)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'cmd_random': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["selections"])
async def cmd_selections(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/selections'"))

        try:
            selections = await bd.getAllSelections()
            await getSelectionsRestaurantsMessage(bot, message, selections)

            await setState(id, 'main', bd)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'cmd_selections': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["top"])
async def cmd_top(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/top'"))

        try:
            await getRestaurantsTopMessage(bot, message)

            await setState(id, 'main', bd)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'cmd_top': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["admin"])
async def cmd_admin(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/admin'"))
        try:
            await setState(id, "main", bd)
            if await isAdmin(id, bd):
                await getCmdAdminMessage(bot, message)
            else:
                await getCmdNoAdminMessage(bot, message)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'cmd_admin': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["info"])
async def cmd_help(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/info'"))
        try:
            await setState(id, "main", bd)
            await getCmdInfoMessage(bot, message)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.info(getLogWithUsersId(id, '-', f"Error in 'cmd_info': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["sticker"])
async def cmd_sticker(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/sticker'"))
        try:
            await setState(id, "main", bd)
            await getCmdStickerMessage(bot, message, await getSticker(0, bd))
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.info(getLogWithUsersId(id, '-', f"Error in 'cmd_sticker': {e}"))
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["location"])
async def cmd_location(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Pressed '/location'"))
        try:
            await setState(id, "location", bd)
            await getCmdLocationMessage(bot, id)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.info(getLogWithUsersId(id, '-', f"Error in 'cmd_location': {e}"))
    else:
        await blockMessage(bot, message)

# WebAppData

@dp.message_handler(content_types="web_app_data")
async def handle_web_app_data(webAppMes):
    id = int(webAppMes.from_user.id)

    if await isAccess(id, bd):
        try:
            data = loads(webAppMes.web_app_data.data)
            logger.info(getLogWithUsersId(id, '=', f"web_app_data: {data}"))

            if data['type'] == 'rest':
                rest_id = int(data['restaurant'].split('-')[-1])
                rest = await bd.getRestaurantById(rest_id)
                promotions = await bd.getRestaurantsPromotionsByRestId(rest["id"])
                await getRestaurantsMessage(bot, id, rest, promotions)
                reviews = await bd.getRestaurantsReviewsByRestId(rest["id"])

                if reviews:
                    await getRestaurantsReviewsMessage(bot, id, reviews)
            elif data['type'] == 'params':
                kitchens, areas = get_kitchens_json(), get_areas_json()
                kitchen, area = "", ""

                for x in kitchens.keys():
                    if kitchens[x]['card_name'] == data['kitchen']:
                        kitchen = kitchens[x]['name']

                for x in areas.keys():
                    if areas[x]['card_name'] == data['area']:
                        area = areas[x]['name']

                if kitchen and area:
                    await getHandleParametersMessage(bot, id, kitchen, area)
                else:
                    raise Exception("Empty parameter!")
        except Exception as e:
            await errorMessage(bot, webAppMes, e)
            logger.info(getLogWithUsersId(id, '-', f"Error in 'cmd_location': {e}"))
    else:
        await blockMessage(bot, webAppMes)

# Текст

@dp.message_handler()
async def handle_text(message: types.Message):
    id = message.from_user.id
    text = message.text

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', f"Text message: {message.text}"))
        try:
            if await isState(id, "search", bd):
                text = text.lower()
                await getListOfRestaurantsMessage(bot, message, text)
                await setState(id, "main", bd)
            else:
                await errorSendingTextMessage(bot, message)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'handle_text': {e}"))
    else:
        await blockMessage(bot, message)

# Фото

@dp.message_handler(content_types=['photo'])
async def handle_photo(message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Photo message"))
        try:
            await errorSendingPhotoMessage(bot, message)
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'handle_photo': {e}"))
    else:
        await blockMessage(bot, message)

# Местоположение

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    id = message.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', f"Location message: {float(message.location['latitude'])}, {float(message.location['longitude'])}"))
        try:
            if await isState(id, "location", bd):
                await getNearRestaurantsMessage(bot, message, message.location['latitude'], message.location['longitude'])
                await setState(id, "main", bd)
            else:
                await bot.send_message(id, "Не то состояние")
        except Exception as e:
            await errorMessage(bot, message, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'handle_location': {e}"))
    else:
        await blockMessage(bot, message)

# Документы

@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_document(doc: types.document.Document):
    id = doc.from_user.id

    if await isAccess(id, bd):
        logger.info(getLogWithUsersId(id, '=', "Document message"))
        try:
            if await isAdmin(id, bd):
                if await isState(id, "doc_users", bd):
                    if doc["document"]["mime_type"] == "application/json":
                        if doc["document"]["file_size"] < 2000000:
                            file_id = doc['document']['file_id']
                            file = await bot.get_file(file_id)
                            file_path = file.file_path
                            test_file_path = f'../data/test_{id}.json'
                            await bot.download_file(file_path, test_file_path)
                            error = isCorrectUsers(test_file_path)
                            if error == "":
                                await contentPathToUsers(test_file_path, bd)
                                await successfulyEditedMessage(bot, doc)
                                await setState(id, "main", bd)
                            else:
                                await errorEditedMessage(bot, doc, f"Ошибка: {error}")
                                logger.warning(getLogWithUsersId(id, '-', f"Error edit {test_file_path}: {error}"))

                            remove(test_file_path)
                        else:
                            await errorEditedMessage(bot, doc, "Подобный файл не может быть такого размера")
                    else:
                        await errorEditedMessage(bot, doc, "Файл должен быть .json")
                else:
                    await errorSendingFileMessage(bot, doc)
            else:
                await getCmdNoAdminMessage(bot, doc)
        except Exception as e:
            test_file_path = f"../data/test_{id}"
            if isfile(test_file_path):
                remove(test_file_path)
            await errorMessage(bot, doc, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'handle_document': {e}"))
    else:
        await blockMessage(bot, doc)

# Callbacks

@dp.callback_query_handler(lambda callback_query: True)
async def handle_callback(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id

    if await isAccess(id, bd):
        user = await bd.getUserById(id)
        logger.info(getLogWithUsersId(id, '=', f"Callback: {callback_query.data}"))
        try:
            admin = await isAdmin(id, bd)
            await setState(id, "main", bd)

            if callback_query.data == 'main':
                await getMainMessage(bot, callback_query)
            elif (len(findall("res_\d+", callback_query.data)) == 1):
                rest = await bd.getRestaurantById(int(callback_query.data.split('_')[-1]))
                promotions = await bd.getRestaurantsPromotionsByRestId(rest["id"])
                await getRestaurantsMessage(bot, id, rest, promotions)
            elif (len(findall("fav_append_\d+", callback_query.data)) == 1):
                rest = await bd.getRestaurantById(int(callback_query.data.split("_")[-1]))
                if str(id) not in rest["favorites"]:
                    rest['favorites'].append(str(id))
                    await writeChangesOfRestaurants(bd, rest)
                if str(rest["id"]) not in user['favorites']:
                    user['favorites'].append(str(rest["id"]))
                    await writeChangesOfUsers(bd, user)
                promotions = await bd.getRestaurantsPromotionsByRestId(rest["id"])
                await getRestaurantsCallback(callback_query, id, rest, promotions)
            elif (len(findall("fav_delete_\d+", callback_query.data)) == 1):
                rest = await bd.getRestaurantById(int(callback_query.data.split("_")[-1]))
                if str(id) in rest["favorites"]:
                    rest['favorites'].remove(str(id))
                    await writeChangesOfRestaurants(bd, rest)
                if str(rest["id"]) in user['favorites']:
                    user['favorites'].remove(str(rest["id"]))
                    await writeChangesOfUsers(bd, user)
                promotions = await bd.getRestaurantsPromotionsByRestId(rest["id"])
                await getRestaurantsCallback(callback_query, id, rest, promotions)
            elif callback_query.data == 'delete_this_message':
                try:
                    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
                except Exception:
                    pass
            elif (len(findall("promotions_\d+", callback_query.data)) == 1):
                rest_id = int(callback_query.data.split('_')[-1])
                promotions = await bd.getRestaurantsPromotionsByRestId(rest_id)
                await getRestaurantsPromotionsMessage(bot, callback_query, promotions)
                await getQuestionBackToRestCardMessage(bot, callback_query, rest_id)
            elif (len(findall("selections_\d+", callback_query.data)) == 1):
                selection_id = int(callback_query.data.split('_')[-1])
                selection = await bd.getSelectionById(selection_id)
                await getSelectionMessage(bot, callback_query, selection)
            elif callback_query.data == 'edit_users' and admin:
                path = f'../data/test_{id}.json'
                await setState(id, "doc_users", bd)
                await contentUsersToPath(bd, path)
                await getUsersEditMessage(bot, path, callback_query)
            elif callback_query.data == 'back_to_admin_panel' and admin:
                await getBackToAdminPanelMessage(callback_query)
            elif (len(findall("social_media_\d+", callback_query.data)) == 1):
                rest_id = int(callback_query.data.split('_')[-1])
                name, social_media = await bd.getRestaurantsSocialMediaByRestId(rest_id)
                await getSocialMediaMessage(bot, callback_query, social_media, name)
            elif (len(findall("back_to_rest_\d+_\d+", callback_query.data)) == 1):
                rest_id = int(callback_query.data.split('_')[-2])
                mes_id = int(callback_query.data.split('_')[-1])
                try:
                    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
                    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=mes_id)
                    rest = await bd.getRestaurantById(rest_id)
                    promotions = await bd.getRestaurantsPromotionsByRestId(rest["id"])
                    await getRestaurantsMessage(bot, id, rest, promotions)
                except Exception:
                    pass
            elif callback_query.data == 'check_users_count':
                count = await bd.getCountOfUsers()
                await getCheckUsersCountMessage(callback_query, count)
            elif callback_query.data == 'check_activity_by_24_hours':
                activity = last24HourUsersActivity()
                await getLast24HourUsersActivityMessage(callback_query, activity)
            elif callback_query.data == 'check_activity_by_week':
                activity = lastWeekUsersActivity()
                await getLastWeekUsersActivityMessage(callback_query, activity)
        except Exception as e:
            await errorMessage(bot, callback_query, e)
            logger.error(getLogWithUsersId(id, '-', f"Error in 'handle_callback': {e}"))
    else:
        await blockMessage(bot, callback_query)

# Служебные

async def on_startup(dp):
    #await bot.set_webhook(WEBHOOK_URL)                 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    await bd.create_pool()
    await bd.check_tables()
    await set_default_commands(dp)
    logger.info(getLog('=', "<-START->"))

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('parameters', '⚙️ Поиск по параметрам'),
            types.BotCommand('search', '🔎 Поиск по названию'),
            types.BotCommand('location', '📍 Рестораны рядом'),
            types.BotCommand('favorites', '⭐️ Избранные рестораны'),
            types.BotCommand('top', '🥇 Топ-10 ресторанов по сохранениям пользователей'),
            types.BotCommand('selections', '⚡️ Подборки ресторанов'),
            types.BotCommand('random', '🎲 Случайный ресторан'),
            types.BotCommand('info', '📄 О боте'),
            types.BotCommand('admin', '👑 Панель администратора')
        ]
    )

async def on_shutdown(dispatcher: Dispatcher):
    await bd.close_pool()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await bot.delete_webhook()
    logger.info(getLog('=', "<-STOP->"))

def getLog(s, text):
    return f"bot.py : [{s}] {text}"

def getLogWithUsersId(id, s, text):
    return f"bot.py : {id} : [{s}] {text}"

if __name__ == "__main__":
    """         <WEBHOOK>
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )"""
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)    # Delete this line for WEBHOOK!
    #on_shutdown(dp)                                                         # Delete this line for WEBHOOK!


'''

                                            # алгоритм Левенштейна
from fuzzywuzzy import fuzz
import asyncio
from unidecode import unidecode
from transliterate import translit

def preprocess_text(text):
    text = text.lower()
    #text = ''.join(c for c in text if c.isalpha() or c.isspace())

    return text

async def calculate_similarity(query, name):
    processed_name = preprocess_text(name)
    len_processed_name = len(processed_name.split(' '))
    len_query = len(query.split(' '))
    similarity_score = 0

    trans_name_ru = unidecode(processed_name)
    trans_name_en = translit(processed_name, 'ru')

    for x in range(len_processed_name):
        first_id = x
        last_id = x + len_query

        if last_id >= len_processed_name:
            similarity_score_ru = fuzz.ratio(query, ' '.join(trans_name_ru.split(' ')[first_id:]))
            similarity_score_en = fuzz.ratio(query, ' '.join(trans_name_en.split(' ')[first_id:]))
            similarity_score = max([similarity_score_ru, similarity_score_en, similarity_score])
            break
        else:
            similarity_score_ru = fuzz.ratio(query, ' '.join(trans_name_ru.split(' ')[first_id:last_id]))
            similarity_score_en = fuzz.ratio(query, ' '.join(trans_name_en.split(' ')[first_id:last_id]))
            similarity_score = max([similarity_score_ru, similarity_score_en, similarity_score])

    return similarity_score, name

async def smart_search(query, restaurant_names):
    query = preprocess_text(query)

    tasks = [calculate_similarity(query, name) for name in restaurant_names]
    results = await asyncio.gather(*tasks)

    main_results = [(score, name) for score, name in results if score >= 50]

    sorted_main_results = sorted(main_results, key=lambda x: x[0], reverse=True)
    print(sorted_main_results)


    sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
    return [result[1] for result in sorted_results]

# Пример использования:
restaurant_names = [
    "Лодка",
    "Китайские новости",
    "Valenok",
    "Folk",
    "Горыныч",
    "Pizza Hut",
    "Рыба моя",
    "Probka",
    "Хачапури и вино",
    "J'Pan",
    "Жирок",
    "Piazza Italiana",
    "Archie",
    "папа джонс",
    "Сыроварня",
    "Modus",
    "Луч",
    "Black Market",
    "Semifreddo",
    "Christian",
    "Il forno",
    "Жеральдин",
    "Vаниль",
    "Тинатин",
    "Hibiki",
    "Novikov",
    "Redbox",
    "Фаренгейт",
    "эZo Georgian Cuizine",
    "Турандот",
    "Техникум",
    "Ketch Up",
    "Loona",
    "Гранд Кафе Dr. Живаго",
    "Cutfish Bistro",
    "Shiba",
    "Gutai",
    "800°С Contemporary Steak",
    "Uilliam’s",
    "Pino",
    "Bro & N",
    "Ava",
    "Patriki",
    "Erwin. Патрики. Павильон. Пруд",
    "Margarita Bistro",
    "Bocconcino",
    "Мари Vanna",
    "Матрешка",
    "Mercedes Bar",
    "Erwin. РекаМореОкеан",
    "Buono",
    "Il forno",
    "Brasserie Lambic",
    "Тбилиси",
    "Black Thai",
    "Soluxe Club",
    "Uhvat",
    "Remy Kitchen Bakery",
    "Sixty",
    "Tutto Bene",
    "Магадан",
    "Дружба",
    "The Toy",
    "Selfie",
    "Bluefin Nikkei",
    "Balzi Rossi",
    "Bamboo.Bar",
    "Белуга",
    "Восход",
    "Bosco Café",
    "Страна которой нет",
    "La Bottega Siciliana",
    "Savva",
    "Taste",
    "Coba hand roll bar",
    "Чемодан",
    "Ugolёk",
    "Maya",
    "ЮГ 22",
    "Niki",
    "Гвидон",
    "She",
]

query = "стоун эйдж"

# Создаем цикл событий для асинхронного выполнения
loop = asyncio.get_event_loop()
results = loop.run_until_complete(smart_search(query, restaurant_names))
#print(results)'''







'''from fuzzywuzzy import fuzz
from unidecode import unidecode
from transliterate import translit

def preprocess_text(text):
    # Переводим текст в нижний регистр и удаляем лишние символы
    text = text.lower()
    text = ''.join(c for c in text if c.isalpha() or c.isspace())
    # Здесь можно добавить дополнительные шаги предобработки, такие как удаление стоп-слов и т.д.
    return text

def smart_search(query, restaurant_names):
    # Предобработка запроса пользователя
    query = preprocess_text(query)

    # Создаем словарь для хранения сходства названий ресторанов с запросом пользователя
    similarity_scores = {}
    main_similarity_scores = {}

    for name in restaurant_names:
        # Предобработка названия ресторана
        processed_name = preprocess_text(name)

        # Транслитерация русских названий ресторанов
        trans_name_ru = unidecode(processed_name)
        print(trans_name_ru)

        # Транслитерация английских названий ресторанов
        trans_name_en = translit(processed_name, 'ru')
        print(trans_name_en)

        # Вычисляем сходство между запросом и транслитерированными названиями ресторана
        similarity_score_ru = fuzz.ratio(query, trans_name_ru)
        similarity_score_en = fuzz.ratio(query, trans_name_en)

        # Выбираем максимальное сходство
        similarity_score = max(similarity_score_ru, similarity_score_en)

        if similarity_score < 60:
            if query in trans_name_en or query in trans_name_ru:
                similarity_score = 60
                main_similarity_scores[name] = similarity_score
        else:
            main_similarity_scores[name] = similarity_score

        similarity_scores[name] = similarity_score

    # Сортируем результаты по убыванию сходства и возвращаем список названий ресторанов
    sorted_results = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    main_sorted_results = sorted(main_similarity_scores.items(), key=lambda x: x[1], reverse=True)
    print(sorted_results)
    print(f"\n\n{main_sorted_results}\n\n")
    return [result[0] for result in sorted_results]

# Пример использования:
restaurant_names = [
    "Лодка",
    "Китайские новости",
    "Valenok",
    "Folk",
    "Горыныч",
    "Рыба моя",
    "Probka",
    "Хачапури и вино",
    "J'Pan",
    "Жирок",
    "Piazza Italiana",
    "Archie",
    "Сыроварня",
    "Modus",
    "Луч",
    "Black Market",
    "Semifreddo",
    "Christian",
    "Il forno",
    "Жеральдин",
    "Vаниль",
    "Тинатин",
    "Hibiki",
]

query = "а"
results = smart_search(query, restaurant_names)
print(results)'''





