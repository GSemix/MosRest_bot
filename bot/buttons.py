# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import urllib.parse

def getCmdParametersButtons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('⚙️ Параметры поиска', web_app=WebAppInfo(url="https://digitalplatforms.su/mos_rest_params/V1"))
    markup.add(button)

    return markup

def getSuccessfulyEditedButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToAdmin()

    markup.add(back)
    return markup

def getCmdAdminButtons():
    list = []

    markup = InlineKeyboardMarkup(row_width=1)
    list.append(InlineKeyboardButton("Корректировать пользователей", callback_data='edit_users'))
    list.append(InlineKeyboardButton("Всего пользователей", callback_data='check_users_count'))
    list.append(InlineKeyboardButton("Активность за последние 24 часа", callback_data='check_activity_by_24_hours'))
    list.append(InlineKeyboardButton("Активность за последнюю неделю", callback_data='check_activity_by_week'))
    markup.add(*list)

    return markup

def getInlineButtonBackToAdmin():
    return InlineKeyboardButton("↩️ Вернуться в панель администратора", callback_data='back_to_admin_panel')

def getRestaurantsPromotionsButtons(url_promotion):
    keyboard = InlineKeyboardMarkup()

    if url_promotion:
        button0 = InlineKeyboardButton('🔍 Смотреть подробнее', url=url_promotion)
        keyboard.add(button0)

    return keyboard

def getQuestionBackToRestCardButtons(mes_id, rest_id):
    keyboard = InlineKeyboardMarkup()
    button0 = InlineKeyboardMarkup(text="Да", callback_data=f'back_to_rest_{rest_id}_{mes_id}')
    button1 = InlineKeyboardMarkup(text="Нет", callback_data=f'delete_this_message')
    keyboard.add(button0)
    keyboard.add(button1)

    return keyboard

def getRestaurantsTopButtons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button = KeyboardButton('🥇 Топ-10 ресторанов по сохранениям пользователей', web_app=WebAppInfo(url="https://digitalplatforms.su/mos_rest_restaurants/V1/?type_page=" + urllib.parse.quote('top')))
    markup.add(button)

    return markup

def getSocialMediaButtons(social_media):
    list = []

    markup = InlineKeyboardMarkup(row_width=1)
    for x in social_media.keys():
        list.append(InlineKeyboardButton(f"{x}", url=social_media[x]))
    markup.add(*list)

    return markup

def getRestaurantsButtons(promotions, url_site, url_map, url_menu, favorites, social_media, res_id):
    keyboard = InlineKeyboardMarkup()

    if favorites:
        button_fav = InlineKeyboardButton('⭐ Удалить из избранного', callback_data=f"fav_delete_{res_id}")
        keyboard.add(button_fav)
    else:
        button_fav = InlineKeyboardButton('⭐ Добавить в избранное', callback_data=f"fav_append_{res_id}")
        keyboard.add(button_fav)

    if promotions:
        button0 = InlineKeyboardButton('😋 Акции и мероприятия', callback_data=f"promotions_{res_id}")
        keyboard.add(button0)
    if social_media:
        button1 = InlineKeyboardButton('📸 Социалные сети', callback_data=f"social_media_{res_id}")
        keyboard.add(button1)
    if url_site != "":
        button2 = InlineKeyboardButton('🌐 Сайт', url=url_site)
        keyboard.add(button2)
    if url_map != "" and len(url_map) > 5:
        if url_map[:5] == "https":
            button3 = InlineKeyboardButton('🌏 На карте', web_app=WebAppInfo(url=url_map))
        else:
            button3 = InlineKeyboardButton('🌏 На карте', url=url_map)
        keyboard.add(button3)
    if url_menu != "" and len(url_menu) > 5:
        if url_menu[:5] == "https":
            button4 = InlineKeyboardButton('🍛 Меню', web_app=WebAppInfo(url=url_menu))
        else:
            button4 = InlineKeyboardButton('🍛 Меню', url=url_menu)
        keyboard.add(button4)
    return keyboard

def getListOfRestaurantsButtons(text):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button = KeyboardButton('🔎 Результат поиска', web_app=WebAppInfo(url='https://digitalplatforms.su/mos_rest_restaurants/V1/?type_page=' + urllib.parse.quote('search') + '&text=' + urllib.parse.quote(str(text))))
    markup.add(button)

    return markup

def getSelectionsRestaurantsButtons(selections):
    markup = InlineKeyboardMarkup(row_width=1)
    list = []

    for selection in selections:
        list.append(InlineKeyboardButton(selection['name'], callback_data=f'selections_{selection["id"]}'))

    markup.add(*list)
    return markup

def getRestaurantsReviewsButtons(reviews):
    markup = InlineKeyboardMarkup(row_width=1)

    for x in reviews:
        markup.add(InlineKeyboardButton(x['author'], url=x['url']))

    return markup

def getSelectionButtons(selection):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button = KeyboardButton(f'📒 {selection["name"]}', web_app=WebAppInfo(url='https://digitalplatforms.su/mos_rest_restaurants/V1/?type_page=' + urllib.parse.quote('selections') + '&id=' + urllib.parse.quote(str(selection['id']))))
    markup.add(button)

    return markup

def getCmdFavoritesButtons(id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button = KeyboardButton('⭐ Избранные рестораны ⭐', web_app=WebAppInfo(url='https://digitalplatforms.su/mos_rest_restaurants/V1/?type_page=' + urllib.parse.quote('favorites') + '&id=' + urllib.parse.quote(str(id))))
    markup.add(button)

    return markup

def getNearRestaurantsButtons(latitude, longitude):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button = KeyboardButton('📍 Рестораны рядом', web_app=WebAppInfo(url='https://digitalplatforms.su/mos_rest_restaurants/V1/?type_page=' + urllib.parse.quote('location') + '&latitude=' + urllib.parse.quote(str(latitude)) + '&longitude=' + urllib.parse.quote(str(longitude))))
    markup.add(button)

    return markup

def getHandleParametersButtons(kitchen, area):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button = KeyboardButton('📋 Рестораны', web_app=WebAppInfo(url='https://digitalplatforms.su/mos_rest_restaurants/V1/?type_page=' + urllib.parse.quote('params') + '&kitchen=' + urllib.parse.quote(kitchen) + '&area=' + urllib.parse.quote(area)))
    markup.add(button)

    return markup

def getCheckUsersCountButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    button0 = getInlineButtonBackToAdmin()

    markup.add(button0)
    return markup

def getLast24HourUsersActivityButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    button0 = getInlineButtonBackToAdmin()

    markup.add(button0)
    return markup

def getLastWeekUsersActivityButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    button0 = getInlineButtonBackToAdmin()

    markup.add(button0)
    return markup

def getCmdLocationButtons():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("Share Position", request_location=True)
    markup.add(button)

    return markup



