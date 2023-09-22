# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.utils import exceptions

from buttons import *
from config_reader import config
from logger import logger

async def errorMessage(bot, message, error):
    await bot.send_message(message.from_user.id, f"<b>Ошибка:</b> {error}", parse_mode = types.ParseMode.HTML)
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'errorMessage'"))

async def getCmdStartMessage(bot, message):
    await bot.send_message(message.from_user.id, "👋 Привет, {0.username}!\nЯ пока не научился поддерживать с тобой диалог, но отлично понимаю <b>команды</b>:".format(message.from_user), parse_mode=types.ParseMode.HTML)
    await bot.send_message(message.from_user.id, """/parameters -> ⚙️ Поиск по параметрам

/search -> 🔎 Поиск по названию

/location -> 📍 Рестораны рядом

/favorites -> ⭐️ Избранные рестораны

/top -> 🥇 Топ-10 ресторанов по сохранениям пользователей

/selections -> ⚡️ Подборки ресторанов

/random -> 🎲 Случайный ресторан

/info -> 📄 О боте""", parse_mode=types.ParseMode.HTML)
    await bot.send_message(message.from_user.id, "🟦 Эти команды ты можешь найти при нажатии на голубую кнопку <b>\"≡ Меню\"</b>, расположенной в левом верхнем углу твоей клавиатуры.""".format(message.from_user), parse_mode=types.ParseMode.HTML)
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'getCmdStartMessage'"))

async def blockMessage(bot, message):
    await bot.send_message(message.from_user.id, f"<b>😨 У вас нет прав доступа, обратитесь к администраторам</b>", parse_mode = types.ParseMode.HTML)
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'blockMessage'"))

async def getCmdParametersMessage(bot, message):
    await bot.send_message(message.from_user.id, "<b>✅ Нажмите на кнопку '⚙️ Параметры поиска', чтобы перейти к их выбору</b>", parse_mode=types.ParseMode.HTML,
                           reply_markup=getCmdParametersButtons())
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'getCmdParametersMessage'"))

async def getCmdAdminMessage(bot, message):
    await bot.send_message(message.from_user.id, "<b>Панель администратора</b>",
                           reply_markup=getCmdAdminButtons())
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'getCmdAdminMessage'"))

async def getCmdNoAdminMessage(bot, message):
    await bot.send_message(message.from_user.id, "Вы не администратор")
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'getCmdNoAdminMessage'"))

async def getQuestionBackToRestCardMessage(bot, callback_query, rest_id):
    await bot.send_message(callback_query.from_user.id , "Вернуться к просмотру карточки ресторана?", reply_markup=getQuestionBackToRestCardButtons(callback_query.message.message_id, rest_id))

async def getCmdInfoMessage(bot, message):
    await bot.send_message(message.from_user.id, """
<b>О боте:</b> данный бот станет Вашим помощником для быстрого и удобного поиска ресторанов Москвы. Бот <b>создан не в коммерческих целях.</b>\nВсе права на названия, логотипы, меню и изображения принадлежат их правообладателям. В случае возникновения каких-либо претензий, просьба связаться с @digital_platforms_bot
<b>О создателях:</b> Мы, команда IT-специалистов, готовы предложить создать telegram bot'a для Вашего уже существующего бизнеса или под новый start up. Еще больше информации можно узнать у @digital_platforms_bot
""", parse_mode = types.ParseMode.HTML)
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'getCmdInfoMessage'"))

async def errorSendingTextMessage(bot, message):
    await bot.send_message(message.from_user.id, "Для отправки текста зайдите в соответствующий пункт")
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'errorSendingTextMessage'"))

async def errorSendingPhotoMessage(bot, message):
    await bot.send_message(message.from_user.id, "Для отправки фото зайдите в соответствующий пункт")
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'errorSendingPhotoMessage'"))

async def getSocialMediaMessage(bot, callback_query, social_media, name):
    await bot.send_message(callback_query.from_user.id , f"📸 Социальные сети '{name}'", reply_markup=getSocialMediaButtons(social_media))

async def successfulyEditedMessage(bot, message):
    await bot.send_message(message.from_user.id, "Успешно", reply_markup=getSuccessfulyEditedButtons())
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'successfulyEditedMessage'"))

async def errorEditedMessage(bot, message, error):
    await bot.send_message(message.from_user.id, f"<b>{error}</b>\nПопробуйте другой файл", parse_mode = types.ParseMode.HTML)
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'errorEditedMessage'"))

async def errorSendingFileMessage(bot, message):
    await bot.send_message(message.from_user.id, "Для отправки файла зайдите в соответствующий пункт")
    logger.info(getLogWithUsersId(message.from_user.id, '+', "Sending 'errorSendingFileMessage'"))

async def getUsersEditMessage(bot, path, callback_query):
    await callback_query.message.edit_text("Измените файл и отправьте его следующим сообщением боту\n<b>Важно! Если в файле будут присутсвовать одинаковые id, то сохранится только последний со всеми его свойствами</b>", parse_mode = types.ParseMode.HTML)
    logger.info(getLogWithUsersId(callback_query.from_user.id, '+', "Sending 'getUsersEditMessage'"))
    await bot.send_document(callback_query.from_user.id, open(path, 'rb'))
    logger.info(getLogWithUsersId(callback_query.from_user.id, '+', f"Sending file {path}"))

async def getBackToAdminPanelMessage(callback_query):
    await callback_query.message.edit_text("<b>Панель администратора</b>", parse_mode = types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getCmdAdminButtons())
    logger.info(getLogWithUsersId(callback_query.from_user.id, '+', "Sending 'getBackToAdminPanelMessage'"))

async def getCmdStickerMessage(bot, message, telegram_id):
    await bot.send_sticker(chat_id=message.from_user.id, sticker=telegram_id['telegram_id'])
    logger.info(getLogWithUsersId(message.from_user.id, '+', f"Sending 'getStickerMessage' with sticker with telegram_id = {telegram_id['telegram_id']}"))

async def getRestaurantsTopMessage(bot, message):
    await bot.send_message(message.from_user.id, f"<b>✅ Нажмите на кнопку '🥇 Топ-10 ресторанов по сохранениям пользователей', чтобы увидеть, что нашлось</b>", parse_mode = types.ParseMode.HTML, reply_markup=getRestaurantsTopButtons())

async def getRestaurantsMessage(bot, id, rest, promotions):
    try:
        image = open(rest["image"], 'rb')
    except:
        image = open("images/testPhoto.jpeg", 'rb')

    text_content = "📓 <b>Название:</b> {}\n\n📍 <b>Адрес:</b> {}".format(rest["name"], rest["address"])

    if rest["average_check"]:
        text_content += "\n\n💸 <b>Средний чек:</b> {} руб (без напитков)".format(rest["average_check"])
    await bot.send_photo(id, image, caption=text_content, parse_mode = types.ParseMode.HTML, reply_markup=getRestaurantsButtons(promotions, rest["url_site"], rest["url_map"], rest["url_menu"], str(id) in rest["favorites"], rest["social_media"], rest["id"]))
    logger.info(getLogWithUsersId(id, '=', f"Get restaurant: {rest['id']}"))
    image.close()

async def getCmdSearchMessage(bot, message):
    await bot.send_message(message.from_user.id, "Введите название ресторана или его часть: ")

async def getRestaurantsReviewsMessage(bot, id, reviews):
    await bot.send_message(id, "👀 <b>Нашлись обзоры на этот ресторан.</b>\nУзнайте мнение авторитетных источников о нем:", parse_mode = types.ParseMode.HTML, reply_markup=getRestaurantsReviewsButtons(reviews))

async def getListOfRestaurantsMessage(bot, message, text):
    await bot.send_message(message.from_user.id, f"<b>✅ Нажмите на кнопку '🔎 Результат поиска', чтобы увидеть, что нашлось</b>", parse_mode = types.ParseMode.HTML, reply_markup=getListOfRestaurantsButtons(text))

async def getSelectionsRestaurantsMessage(bot, message, selections):
    await bot.send_message(message.from_user.id, "⚡️<b>Здесь представлены все самые интересные подборки</b>, выберите какую-нибудь:", reply_markup=getSelectionsRestaurantsButtons(selections), parse_mode = types.ParseMode.HTML)

async def getRestaurantsPromotionsMessage(bot, callback_query, promotions):
    for promotion in promotions:
        text = ""

        if promotion['description']:
            if 'header' in promotion['description'].keys() and promotion['description']['header']:
                text += f"<b>{promotion['description']['header']}</b>\n\n"
            if 'main_text' in promotion['description'].keys() and promotion['description']['main_text']:
                text += f"<em>{promotion['description']['main_text']}</em>"

        if promotion['media']:
            with open(promotion['media'], 'rb') as image:
                await bot.send_photo(callback_query.from_user.id, image, caption=text, parse_mode = types.ParseMode.HTML, reply_markup=getRestaurantsPromotionsButtons(promotion['url']))
        else:
            if text != "":
                await bot.send_message(callback_query.from_user.id, text, parse_mode = types.ParseMode.HTML, reply_markup=getRestaurantsPromotionsButtons(promotion['url']))

        logger.info(getLogWithUsersId(callback_query.from_user.id, '=', f"Get promotion with id {promotion['id']}"))

async def getRestaurantsCallback(callback_query, id, rest, promotions):
    await callback_query.message.edit_reply_markup(reply_markup=getRestaurantsButtons(promotions, rest["url_site"], rest["url_map"], rest["url_menu"], str(id) in rest["favorites"], rest["social_media"], rest["id"]))

async def getCmdFavoritesMessage(bot, message):
    await bot.send_message(message.from_user.id, "<b>✅ Нажмите на кнопку '⭐ Избранные рестораны ⭐', чтобы увидеть результат</b>", reply_markup=getCmdFavoritesButtons(message.from_user.id))

async def getCmdEmptyFavoritesMessage(bot, message):
    await bot.send_message(message.from_user.id, "🤔 Хм, пока здесь ничего нет")

async def getSelectionMessage(bot, callback_query, selection):
    await bot.send_message(callback_query.from_user.id, f"<b>✅ Нажмите на кнопку '📒 {selection['name']}', чтобы увидеть подборку</b>", parse_mode = types.ParseMode.HTML, reply_markup=getSelectionButtons(selection))

async def getGooseMessage(bot, id):
    await bot.send_message(message.from_user.id, "А вот и гусь!")

async def getNearRestaurantsMessage(bot, message, latitude, longitude):
    await message.answer(f"🗺 Ваши координаты: {latitude}, {longitude}\n <b>✅ Нажмите на кнопку '📍 Рестораны рядом', чтобы увидеть результат</b>", parse_mode = types.ParseMode.HTML, reply_markup=getNearRestaurantsButtons(latitude, longitude))

async def getHandleParametersMessage(bot, id, kitchen, area):
    await bot.send_message(id, "<b>⚙️ Параметры поиска\n\n</b><b>🍽 Кухня:</b> {}\n<b>📍Район:</b> {}\n\n<b>✅ Нажмите на кнопку '📋 Рестораны', чтобы увидеть, что нашлось</b>".format(kitchen, area), parse_mode = types.ParseMode.HTML, reply_markup=getHandleParametersButtons(kitchen, area))

async def getCmdLocationMessage(bot, id):
    await bot.send_message(id, "✅ Нажмите на кнопку 'Share Position', чтобы поделиться своей геопозицией", reply_markup=getCmdLocationButtons())

async def getCheckUsersCountMessage(callback_query, count):
    await callback_query.message.edit_text(f"Всего: {count}", parse_mode = types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getCheckUsersCountButtons())
    logger.info(getLogWithUsersId(callback_query.from_user.id, '+', "Sending 'getCheckUsersCountMessage'"))

async def getLast24HourUsersActivityMessage(callback_query, activity):
    text_content = f"<b>| - Команды - |</b> [Всего]: {activity['commands']['all']}\n\n"

    for x in activity['commands'].keys():
        if x != 'all':
            text_content += f"{x} -> {activity['commands'][x]}\n"

    text_content += f"\n<b>| - Рестораны - |</b> [Всего]: {activity['restaurants']['all']}\n\n"

    for x in activity['restaurants'].keys():
        if x != 'all':
            text_content += f"{x} -> {activity['restaurants'][x]}\n"

    #text_content += f"\n<b>| - Новые пользователи - |</b> [Всего]: {activity['users']['all']}"

    await callback_query.message.edit_text(text_content, parse_mode = types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getLast24HourUsersActivityButtons())
    logger.info(getLogWithUsersId(callback_query.from_user.id, '+', "Sending 'getLast24HourUsersActivityMessage'"))

async def getLastWeekUsersActivityMessage(callback_query, activity):
    text_content = f"<b>| - Команды - |</b> [Всего]: {activity['commands']['all']}\n\n"

    for x in activity['commands'].keys():
        if x != 'all':
            text_content += f"{x} -> {activity['commands'][x]}\n"

    text_content += f"\n<b>| - Рестораны - |</b> [Всего]: {activity['restaurants']['all']}\n\n"

    for x in activity['restaurants'].keys():
        if x != 'all':
            text_content += f"{x} -> {activity['restaurants'][x]}\n"

    #text_content += f"\n<b>| - Новые пользователи - |</b> [Всего]: {activity['users']['all']}"

    await callback_query.message.edit_text(text_content, parse_mode = types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getLastWeekUsersActivityButtons())
    logger.info(getLogWithUsersId(callback_query.from_user.id, '+', "Sending 'getLastWeekUsersActivityMessage'"))

def getLogWithUsersId(id, s, text):
    return f"messages.py : {id} : [{s}] {text}"












