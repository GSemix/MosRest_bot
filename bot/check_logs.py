#!/usr/bin/python3
# -*- coding: utf-8 -*-

from file import getData
from config_reader import config
from datetime import datetime

def getDateNow():
	return [str(datetime.now())]

def getDateFromMessage(date):
	data_to_return = {
		'year': 0,
		'month': 0,
		'day': 0,
		'hours': 0,
		'minutes': 0 
	}

	all_date = date[0].split(' ')
	all_day = all_date[0].split('-')
	time = all_date[1].split(':')

	data_to_return['year'] = int(all_day[0])
	data_to_return['month'] = int(all_day[1])
	data_to_return['day'] = int(all_day[2])
	data_to_return['hours'] = int(time[0])
	data_to_return['minutes'] = int(time[1])

	return data_to_return

def getDateWeekBefore(data):
	date = getDateNow()
	data_to_return = getDateFromMessage(date)

	data_to_return['day'] -= 7

	if data_to_return['day'] <= 0:
		data_to_return['day'] += 30
		data_to_return['month'] -= 1

	if data_to_return['month'] == 0:
		data_to_return['month'] = 12
		data_to_return['year'] -= 1

	return data_to_return

def getDate24HoursBefore(data):
	date = getDateNow()
	data_to_return = getDateFromMessage(date)

	data_to_return['day'] -= 1

	if data_to_return['day'] == 0:
		data_to_return['day'] = 30
		data_to_return['month'] -= 1

	if data_to_return['month'] == 0:
		data_to_return['year'] -= 1

	return data_to_return

def fullDateToMinutes(date):
	return date['year'] * 12 * 30 * 24 * 60 + date['month'] * 30 * 24 * 60 + date['day'] * 24 * 60 + date['hours'] * 60 + date['minutes']

def last24HourUsersActivity():
	data_to_return = {
		'commands': {
			'all': 0
		},
		'restaurants': {
			'all': 0
		},
		'users': {
			'all': 0
		}
	}

	data = getData(f"{config.LOGS_PATH.get_secret_value()}logger.out")
	splited_data = data.split('\n')
	min_date = getDate24HoursBefore(splited_data)
	min_data_in_minutes = fullDateToMinutes(min_date)

	for x in splited_data:
		x_splited_data = x.split(' : ')

		if len(x_splited_data) == 5:
			x_date = getDateFromMessage(x_splited_data)
			x_date_in_minutes = fullDateToMinutes(x_date)

			if x_date_in_minutes >= min_data_in_minutes:
				date = x_splited_data[0]
				id = x_splited_data[3]
				message = x_splited_data[4]

				if id not in ['490483818', '879707829']:
					if "Pressed" in message:
						cmd = message.split("'")[-2]

						if cmd not in data_to_return['commands'].keys():
							data_to_return['commands'][cmd] = 1
						else:
							data_to_return['commands'][cmd] += 1

						data_to_return['commands']['all'] += 1
					elif "Get restaurant" in message:
						rest_id = message.split(" ")[-1]

						if rest_id not in data_to_return['restaurants'].keys():
							data_to_return['restaurants'][rest_id] = 1
						else:
							data_to_return['restaurants'][rest_id] += 1

						data_to_return['restaurants']['all'] += 1
					#elif "Append user" in message:
						#data_to_return['0']['all'] += 1

	return data_to_return

def lastWeekUsersActivity():
	data_to_return = {
		'commands': {
			'all': 0
		},
		'restaurants': {
			'all': 0
		},
		'users': {
			'all': 0
		}
	}

	data = getData(f"{config.LOGS_PATH.get_secret_value()}logger.out")
	splited_data = data.split('\n')
	min_date = getDateWeekBefore(splited_data)
	min_data_in_minutes = fullDateToMinutes(min_date)

	for x in splited_data:
		x_splited_data = x.split(' : ')

		if len(x_splited_data) == 5:
			x_date = getDateFromMessage(x_splited_data)
			x_date_in_minutes = fullDateToMinutes(x_date)

			if x_date_in_minutes >= min_data_in_minutes:
				date = x_splited_data[0]
				id = x_splited_data[3]
				message = x_splited_data[4]

				if id not in ['490483818', '879707829']:
					if "Pressed" in message:
						cmd = message.split("'")[-2]

						if cmd not in data_to_return['commands'].keys():
							data_to_return['commands'][cmd] = 1
						else:
							data_to_return['commands'][cmd] += 1

						data_to_return['commands']['all'] += 1
					elif "Get restaurant" in message:
						rest_id = message.split(" ")[-1]

						if rest_id not in data_to_return['restaurants'].keys():
							data_to_return['restaurants'][rest_id] = 1
						else:
							data_to_return['restaurants'][rest_id] += 1

						data_to_return['restaurants']['all'] += 1
					#elif "Append user" in message:
						#data_to_return['0']['all'] += 1

	return data_to_return

#if __name__ == "__main__":
	#print(last24HourUsersActivity())
	#print(lastWeekUsersActivity())
