# -*- coding: utf-8 -*-

import asyncpg
import asyncio

from fuzzywuzzy import fuzz         # Алгоритм Левенштейна
from unidecode import unidecode
from transliterate import translit

import logging
import logging.handlers
from sys import exit as sexit
from os import system
from random import randint
from time import sleep
from json import loads
from json import dumps

from logger import logger
from other import isInt
from templates import *
from config_reader import config

params = {
    'host': config.POSTGRESQL_HOST.get_secret_value(),
    'port': config.POSTGRESQL_PORT.get_secret_value(),
    'user': config.POSTGRESQL_USER.get_secret_value(),
    'password': config.POSTGRESQL_PASSWORD.get_secret_value(),
    'database': config.POSTGRESQL_DATABASE.get_secret_value(),
    'min_size': 3,      # Минимальный размер пула соединений
    'max_size': 10,     # Максимальный размер пула соединений
    'max_queries': 500  # Максимальное количество запросов для одного соединения
}

def getLog(s, text):
    return f"db.py : [{s}] {text}"

class BD(object):
    def __init__(self, params):
        self.params = params
        self.pool = None

    def __setattr__(self, key, value): # Вызывается при изменении <key> класса
        self.__dict__[key] = value

    async def check_tables(self):
        if not await self.table_exists("users", params['database']):
            if await self.create_table_users() == 0:
                logger.info(getLog('+', "Table 'users' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'users' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'users' was detected"))

        if not await self.table_exists("stickers", params['database']):
            if await self.create_table_stikers() == 0:
                logger.info(getLog('+', "Table 'stickers' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'stickers' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'stickers' was detected"))

        if not await self.table_exists("restaurants", params['database']):
            if await self.create_table_restaurants() == 0:
                logger.info(getLog('+', "Table 'restaurants' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'restaurants' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'restaurants' was detected"))

        if not await self.table_exists("reviews", params['database']):
            if await self.create_table_reviews() == 0:
                logger.info(getLog('+', "Table 'reviews' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'reviews' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'reviews' was detected"))

        if not await self.table_exists("promotions", params['database']):
            if await self.create_table_promotions() == 0:
                logger.info(getLog('+', "Table 'promotions' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'promotions' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'promotions' was detected"))

        if not await self.table_exists("selections", params['database']):
            if await self.create_table_selections() == 0:
                logger.info(getLog('+', "Table 'selections' was created"))
            else:
                logger.critical(getLog('-', "Error! Table 'selections' wasn't created"))
        else:
            logger.info(getLog('+', "Table 'selections' was detected"))

    #  Users

    async def create_table_users(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""CREATE TABLE IF NOT EXISTS users(
                        id BIGINT PRIMARY KEY,
                        username TEXT,
                        kitchen TEXT,
                        area TEXT,
                        access BOOLEAN NOT NULL,
                        admin BOOLEAN NOT NULL,
                        state TEXT,
                        favorites TEXT[]);
                    """)

                    return 0
        except asyncpg.PostgresError as e:
            logger.error(getLog('-', f"Error in BD.create_table_users(...): {e}"))
        return None

    async def append_users_item(self, user):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    if not await self.isTwinId("users", user['id']):
                        await connection.execute("INSERT INTO users VALUES($1, $2, $3, $4, $5, $6, $7, $8);", user['id'], user['username'], user['kitchen'], user['area'], user['access'], user['admin'], user['state'], user['favorites'])
                        logger.info(getLog('+', f"Append user: {user}"))
                        return 0
                    else:
                        logger.info(getLog('?', f"Impossible to append item in users: id {user['id']} will be Twin!"))
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.append_users_item(...): {e}"))
        return None

    async def isAdminById(self, id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT admin FROM users WHERE id=$1;", id)

                    if result:
                        if dict(result)['admin']:
                            return True
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.isAdminById(...): {e}"))
        return False

    async def isAccessById(self, id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT access FROM users WHERE id=$1;", id)
                    if result:
                        if dict(result)['access']:
                            return True
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.isAccessById(...): {e}"))
        return False

    async def getCountOfUsers(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT count(*) FROM users;")

                    if result:
                        return dict(result)['count']
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.isAccessById(...): {e}"))
        return 0

    async def getUserById(self, id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT * FROM users WHERE id=$1;", id)

                    if result:
                        return dict(result)
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getUserById(...): {e}"))
        return None

    async def getAllUsersId(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT id FROM users;")
                    
                    if result:
                        return [dict(user)['id'] for user in result]
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getAllUsersId(...): {e}"))

        return []

    async def getAllUsers(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT * FROM users;")
                    
                    if result:
                        return [dict(user) for user in result]
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getAllUsers(...): {e}"))

        return []

    #  Restaurants

    async def create_table_restaurants(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""CREATE TABLE IF NOT EXISTS restaurants(
                        id serial PRIMARY KEY,
                        name TEXT,
                        image TEXT,
                        url_map TEXT,
                        url_site TEXT,
                        url_menu TEXT,
                        address TEXT,
                        area TEXT,
                        kitchen TEXT[],
                        description TEXT,
                        lat_longitude TEXT,
                        favorites TEXT[],
                        average_check INT,
                        social_media JSON);
                    """)

                    return 0
        except asyncpg.PostgresError as e:
            logger.error(getLog('-', f"Error in BD.create_table_restaurants(...): {e}"))
        return None

    async def append_restaurants_item(self, restaurant):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("INSERT INTO restaurants(name, image, url_map, url_site, url_menu, address, area, kitchen, description, lat_longitude, favorites, average_check, social_media) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13);", restaurant['name'], restaurant['image'], restaurant['url_map'], restaurant['url_site'], restaurant['url_menu'], restaurant['address'], restaurant['area'], restaurant['kitchen'], restaurant['description'], restaurant['lat_longitude'], restaurant['favorites'], restaurant['average_check'], restaurant['social_media'])
                    logger.info(getLog('+', f"Append restaurant: {restaurant}"))
                    return 0
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.append_restaurants_item(...): {e}"))
        return None

    async def getRestaurantById(self, id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT * FROM restaurants WHERE id=$1;", id)

                    if result:
                        result = dict(result)
                        if result['social_media']:
                            result['social_media'] = loads(result['social_media'])
                        return result
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantById(...): {e}"))
        return None

    async def getRestaurantsLocation(self):
        list_result = []

        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT id, name, address, image, lat_longitude FROM restaurants;")

                    if result:
                        result = [dict(rest) for rest in result]

                        for x in result:
                            lat_longitude = x['lat_longitude'].split(', ')

                            if lat_longitude != ['']:
                                list_result.append({
                                    'id': x['id'],
                                    'name': x['name'],
                                    'address': x['address'],
                                    'image': x['image'],
                                    'latitude': float(lat_longitude[0]),
                                    'longitude': float(lat_longitude[1])
                                })
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantsLocation(...): {e}"))
        return list_result

    async def getRandomRestaurant(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT MAX(id) FROM restaurants;")

            if result:
                rand_id = randint(1, dict(result)['max'])
                async with self.pool.acquire() as connection:
                    async with connection.transaction():
                        result = await connection.fetchrow("SELECT * FROM restaurants WHERE id=$1;", rand_id)

                        if result:
                            return dict(result)
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRandomRestaurant(...): {e}"))
        return None

    async def getTop10Restaurant(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT id, name, address, image, favorites FROM restaurants;")
                    result = [dict(rest) for rest in result]
                    result.sort(key=lambda x: len(x['favorites']))
                    result.reverse()
                    result = result[0:10]

                    for x in result:
                        x['score'] = len(x['favorites'])
                        del x['favorites']

                    return result
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRandomRestaurant(...): {e}"))
        return None

    async def getRestaurantsByName(self, name):
        def preprocess_text(text):
            text = text.lower()
            #text = ''.join(c for c in text if c.isalpha() or c.isspace())
            return text

        async def calculate_similarity(query, restaurant):
            processed_name = preprocess_text(restaurant['name'])
            len_processed_name = len(processed_name.split(' '))
            len_query = len(query.split(' '))
            restaurant['similarity_score'] = 0

            trans_name_ru = unidecode(processed_name)
            trans_name_en = translit(processed_name, 'ru')

            for x in range(len_processed_name):
                first_id = x
                last_id = x + len_query

                if last_id >= len_processed_name:
                    similarity_score_ru = fuzz.ratio(query, ' '.join(trans_name_ru.split(' ')[first_id:]))
                    similarity_score_en = fuzz.ratio(query, ' '.join(trans_name_en.split(' ')[first_id:]))
                    restaurant['similarity_score'] = max([similarity_score_ru, similarity_score_en, restaurant['similarity_score']])
                    break
                else:
                    similarity_score_ru = fuzz.ratio(query, ' '.join(trans_name_ru.split(' ')[first_id:last_id]))
                    similarity_score_en = fuzz.ratio(query, ' '.join(trans_name_en.split(' ')[first_id:last_id]))
                    restaurant['similarity_score'] = max([similarity_score_ru, similarity_score_en, restaurant['similarity_score']])

            return restaurant

        async def smart_search(query, restaurant_names):
            query = preprocess_text(query)

            tasks = [calculate_similarity(query, restaurant) for restaurant in restaurant_names]
            results = await asyncio.gather(*tasks)

            main_results = [restaurant for restaurant in results if restaurant["similarity_score"] >= 70]
            mb_results = [restaurant for restaurant in results if restaurant["similarity_score"] >= 50 and restaurant["similarity_score"] < 70]

            for restaurant in main_results:
                result = await self.getRestaurantById(restaurant['id'])

                if result:
                    for key in result.keys():
                        restaurant[key] = result[key]

            for restaurant in mb_results:
                result = await self.getRestaurantById(restaurant['id'])

                if result:
                    for key in result.keys():
                        restaurant[key] = result[key]

            sorted_main_results = sorted(main_results, key=lambda x: x['similarity_score'], reverse=True)
            sorted_mb_results = sorted(mb_results, key=lambda x: x['similarity_score'], reverse=True)
            return (sorted_main_results, sorted_mb_results)

        query = preprocess_text(name)
        restaurants_data = []

        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    #result = await connection.fetch("SELECT * FROM restaurants WHERE name ILIKE $1;", f"%{name_escaped}%") # Исправить уязвимость
                    result = await connection.fetch("SELECT id, name FROM restaurants;")

                    restaurant_names = [dict(restaurant) for restaurant in result]
                    restaurant_data = await smart_search(query, restaurant_names)

                    return restaurant_data
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantsByName(...): {e}"))
        return restaurants_data

    async def getRestaurantsByKitchenAndArea(self, kitchen, area):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    if kitchen == "Любая" and area == "Любой":
                        result = await connection.fetch("SELECT * FROM restaurants;")
                    elif area == "Любой":
                        result = await connection.fetch("SELECT * FROM restaurants WHERE kitchen && ARRAY[$1];", kitchen)
                    elif kitchen == "Любая":
                        result = await connection.fetch("SELECT * FROM restaurants WHERE area=$1;", area)
                    else:
                        result = await connection.fetch("SELECT * FROM restaurants WHERE kitchen && ARRAY[$1] AND area=$2;", kitchen, area)

                    if result:
                        return [dict(rest) for rest in result]
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantsByKitchenAndArea(...): {e}"))
        return []

    async def getAreasByKitchen(self, kitchen):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    if kitchen == "Любая":
                        result = await connection.fetch("SELECT * FROM restaurants;")
                    else:
                        result = await connection.fetch("SELECT * FROM restaurants WHERE kitchen && ARRAY[$1];", kitchen)

                    if result:
                        return set([dict(rest)['area'] for rest in result])
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getAreasByKitchen(...): {e}"))
        return []

    async def getAllRestaurantsId(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT id FROM restaurants;")

                    if result:
                        return [dict(rest)['id'] for rest in result]
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getAllRestaurantsId(...): {e}"))
        return []

    async def getRestaurantsSocialMediaByRestId(self, rest_id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT name, social_media FROM restaurants WHERE id=$1;", rest_id)

                    if result:
                        result = dict(result)
                        return result["name"], loads(result["social_media"])
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantsPromotionsByRestId(...): {e}"))
        return None

    #  Stickers

    async def create_table_stikers(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""CREATE TABLE IF NOT EXISTS stickers(
                        id serial PRIMARY KEY,
                        telegram_id TEXT,
                        name TEXT,
                        family TEXT);
                    """)

                    return 0
        except asyncpg.PostgresError as e:
            logger.error(getLog('-', f"Error in BD.create_table_stikers(...): {e}"))
        return None

    async def append_stickers_item(self, sticker):
        try:
            if not await self.isTwinTelegramId(sticker['telegram_id']):
                async with self.pool.acquire() as connection:
                    async with connection.transaction():
                        await connection.execute("INSERT INTO stickers(telegram_id, name, family) VALUES($1, $2, $3);", sticker['telegram_id'], sticker['name'], sticker['family'])
                        logger.info(getLog('+', f"Append sticker: {sticker}"))
                        return 0
            else:
                logger.info(getLog('?', f"Impossible to append item in stickers: telegram_id {sticker['telegram_id']} will be Twin!"))
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.append_stickers_item(...): {e}"))
        return None

    async def get_sticker_by_name_and_family(self, name, family):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT * FROM stickers WHERE name = $1 AND family = $2;", name, family)

                    if result:
                        return dict(result)
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.get_sticker_by_name_and_family(...): {e}"))
        return None


    async def isTwinTelegramId(self, telegram_id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT * FROM stickers WHERE telegram_id=$1;", telegram_id)

                    if result:
                        return True
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.isTwinTelegramId(...): {e}"))
        return False

    #  Reviews

    async def create_table_reviews(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""CREATE TABLE IF NOT EXISTS reviews(
                        id serial PRIMARY KEY,
                        rest_id INT,
                        author TEXT,
                        url TEXT);
                    """)

                    return 0
        except asyncpg.PostgresError as e:
            logger.error(getLog('-', f"Error in BD.create_table_reviews(...): {e}"))
        return None

    async def getRestaurantsReviewsById(self, id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT * FROM promotions WHERE id=$1;", id)

                    if result:
                        return dict(result)
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantsReviewsById(...): {e}"))
        return None

    async def getRestaurantsReviewsByRestId(self, rest_id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT * FROM reviews WHERE rest_id=$1;", rest_id)

                    if result:
                        return [dict(review) for review in result]
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantsReviewsByRestId(...): {e}"))
        return []

    #  Promotions

    async def create_table_promotions(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""CREATE TABLE IF NOT EXISTS promotions(
                        id serial PRIMARY KEY,
                        rest_id INT,
                        media TEXT,
                        description JSON,
                        url TEXT);
                    """)

                    return 0
        except asyncpg.PostgresError as e:
            logger.error(getLog('-', f"Error in BD.create_table_promotions(...): {e}"))
        return None

    async def getRestaurantsPromotionsById(self, id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT * FROM promotions WHERE id=$1;", id)

                    if result:
                        result = dict(result)
                        result["description"] = loads(result["description"])

                        return result
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantsPromotionsById(...): {e}"))
        return None   

    async def getRestaurantsPromotionsByRestId(self, rest_id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT * FROM promotions WHERE rest_id=$1;", rest_id)

                    if result:
                        result = [dict(promotion) for promotion in result]

                        for promotion in result:
                            promotion["description"] = loads(promotion["description"])

                        return result
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getRestaurantsPromotionsByRestId(...): {e}"))
        return []

    #  Selections

    async def create_table_selections(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("""CREATE TABLE IF NOT EXISTS selections(
                        id serial PRIMARY KEY,
                        name TEXT,
                        type_selection TEXT,
                        author TEXT,
                        id_list INT[]);
                    """)

                    return 0
        except asyncpg.PostgresError as e:
            logger.error(getLog('-', f"Error in BD.create_table_selections(...): {e}"))
        return None

    async def getAllSelections(self):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch("SELECT * FROM selections;")

                    if result:
                        result = [dict(selection) for selection in result]
                        return result
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getSelectionById(...): {e}"))
        return None

    async def getSelectionById(self, id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow("SELECT * FROM selections WHERE id=$1;", id)

                    if result:
                        result = dict(result)
                        return result
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.getSelectionById(...): {e}"))
        return None

    #  Универсальные

    async def isTwinId(self, table, id):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetchrow(f"SELECT * FROM {table} WHERE id=$1;", id)

                    if result:
                        return True
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.isTwinId(...): {e}"))
        return False

    async def table_exists(self, table, database): # Проверяет, существует ли table
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch(f"SELECT * FROM information_schema.tables WHERE table_name = '{table}' AND table_catalog = '{database}';")

                    if result:
                        return True
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.table_exists(...): {e}"))
        return False

    async def update_column_by_id(self, column, table, newValue, id):
        if isInt(id):
            try:
                async with self.pool.acquire() as connection:
                    async with connection.transaction():
                        await connection.execute(f"UPDATE {table} SET {column} = $1 WHERE id = $2", newValue, id) # Исправить уязвимость
                        logger.info(getLog('+', f"Update users with id = {id} column {column} > {newValue}"))
                        return 0
            except asyncpg.PostgresError as e:
                logger.warning(getLog('-', f"Error in BD.update_column_by_id(...): {e}"))
        return None

    async def get_all(self, table):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch(f"SELECT * FROM {table};") # Исправить уязвимость

                    if result:
                        return [dict(row) for row in result]
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.get_all(...): {e}"))
            return None

    async def get_column_by_id(self, column, table, id):
        if isInt(id):
            try:
                async with self.pool.acquire() as connection:
                    async with connection.transaction():
                        result = await connection.fetchrow(f"SELECT {column} FROM {table} WHERE id=$1;", id) # Исправить уязвимость

                        if result:
                            return dict(result)[f'{column}']
            except asyncpg.PostgresError as e:
                logger.warning(getLog('-', f"Error in BD.get_column_by_id(...): {e}"))
        return None

    async def delete_item_by_id(self, table, id):
        if isInt(id):
            try:
                async with self.pool.acquire() as connection:
                    async with connection.transaction():
                        await connection.execute(f"DELETE FROM {table} WHERE id=$1;", id) # Исправить уязвимость
                        logger.info(getLog('+', f"Delete row with id = {id} from tabel '{table}'"))
                        return 0
            except asyncpg.PostgresError as e:
                logger.warning(getLog('-', f"Error in BD.delete_item_by_id(...): {e}"))
        return None

    async def delete_item_by_name(self, table, name):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(f"DELETE FROM {table} WHERE name=$1;", name)
                    logger.info(getLog('+', f"Delete row with name = {name} from tabel '{table}'"))
                    return 0
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.delete_item_by_name(...): {e}"))
        return None

    async def rename_column(self, table, old_column, new_column):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(f"ALTER TABLE {table} RENAME COLUMN {old_column} TO {new_column};") # Исправить уязвимость
                    logger.info(getLog('+', f"Column '{old_column}' from table '{table}' was renamed to '{new_column}'"))
                    return 0
        except asyncpg.PostgresError as e:
            logger.warning(getLog('-', f"Error in BD.rename_column(...): {e}"))
            return None

    async def create_pool(self):
        #self.params['init'] = self.set_client_encoding
        self.pool = await asyncpg.create_pool(**self.params)

    async def close_pool(self):
        await self.pool.close()

'''
# Создаем объект UserDatabase и запускаем асинхронный цикл событий aiogram
async def main():
    dsn = "postgres://mos_rest:54610627Qwerty@digitalplatforms.su/mos_rest"  # Замените данными вашей базы данных
    user_db = BD(params)
    await user_db.create_pool()
    await user_db.check_tables()

    try:

        await user_db.append_users_item({
            'id': 1234,
            'username': 'qwe',
            'kitchen': 'asd',
            'area': 'zxc',
            'access': True,
            'admin': True,
            'state': 'iop',
            'favorites': ['aaa', 'bbb'],
            })
        await user_db.isAdminById(12345)
        await user_db.getCountOfUsers()
        await user_db.getUserById(123)
        await user_db.getAllUsersId()
        await user_db.append_restaurants_item({
            'name': 'qwe',
            'image': 'qwe',
            'url_map': 'qwe',
            'url_site': 'qwe',
            'url_menu': 'qwe',
            'address': 'qwe',
            'area': 'qwe',
            'kitchen': ['qwe', 'asd'],
            'description': 'qwe',
            'lat_longitude': '55.766564, 37.623201',
            'favorites': ['123', '123'],
            'reviews': ['{"user": "John", "rating": 5, "comment": "Great place!"}']
            })
        await user_db.getRestaurantById(55)
        await user_db.getRestaurantsLocation()
        await user_db.getRandomRestaurant()
        await user_db.getTop10Restaurant()
        await user_db.getRestaurantsByName('Лодка')
        await user_db.getRestaurantsByKitchenAndArea('Авторская', 'Тверская улица')
        await user_db.getAreasByKitchen('Авторская')
        await user_db.getAllRestaurantsId()
        await user_db.getRestaurantsReviewsById(1)
        await user_db.isTwinTelegramId('asd')
        await user_db.append_stickers_item({
            'telegram_id': 'aaa',
            'name': 'bbb',
            'family': 'ccc'
            })
        await user_db.update_column_by_id('family', 'stickers', "new_value", 1)
        print(await user_db.get_all('stickers'))
        print(await user_db.get_column_by_id('family', 'stickers', 1))
        await user_db.delete_item_by_id("stickers", 2)
        await user_db.delete_item_by_name("stickers", 'asd')
        await user_db.rename_column("stickers", "gg", "family")
    finally:
        await user_db.close_pool()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
'''