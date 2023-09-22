# -*- coding: utf-8 -*-

from json import dump
from json import load

from config_reader import config

def getJsonData(file_name):
    with open(file_name, 'r') as file:
        data = load(file)

    return data

def getJsonDataWithIntKeys(file_name):
    data = getJsonData(file_name)

    return convertJsonDataToKeyInt(data)

def writeJsonData(file_name, data):
    with open(file_name, 'w', encoding='utf8') as file:
        dump(data, file, ensure_ascii=False, indent=4)

def convertJsonDataToKeyInt(data):
    new = {}
    for x in data.keys():
        new[int(x)] = data[x]

    return new

def getData(file_name):
    with open(file_name, 'r') as file:
        data = file.read()

    return data

def setData(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)

def get_kitchens_json():
    return getJsonData("../data/kitchens.json")

def get_areas_json():
    return getJsonData("../data/areas.json")