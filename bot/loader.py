#!/usr/bin/python3
# -*- coding: utf-8 -*-

from db import BD
from config_reader import config
from sys import argv
from file import getJsonDataWithIntKeys

if __name__ == "__main__":
	what = argv[1]
	path = argv[2]
	data = getJsonDataWithIntKeys(path)

	params = {
	    'host': config.POSTGRESQL_HOST.get_secret_value(),
	    'port': config.POSTGRESQL_PORT.get_secret_value(),
	    'user': config.POSTGRESQL_USER.get_secret_value(),
	    'password': config.POSTGRESQL_PASSWORD.get_secret_value(),
	    'database': config.POSTGRESQL_DATABASE.get_secret_value()
	}

	bd = BD(params)

	if what == "users":
		for x in data.keys():
			user = [x, data[x]['name'], data[x]['kitchen'], data[x]['area'], True, False, data[x]['part'], data[x]['favorites']]
			bd.append_users_item(user)
	elif what == "rest":
		for x in data.keys():
			res = [data[x]['name'], data[x]['image'], data[x]['url_map'], data[x]['url_site'], data[x]['url_menu'], data[x]['address'], data[x]['area'], data[x]['kitchen'], data[x]['description'], data[x]['lat/longitude'], data[x]['favorites']]
			bd.append_restaurants_item(res)
	else:
		print(f"Error -> What is '{what}'?")

