# -*- coding: utf-8 -*-

from jsonschema import validate
from json import loads
from json import dumps

from file import getJsonData
from file import getJsonDataWithIntKeys
from file import writeJsonData
from file import getData
from file import setData
from config_reader import config
from templates import *

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

async def getUsersId(bd):
    return await bd.getAllUsersId()

async def getUsers(bd):
    return await bd.getAllUsers()

async def setUser(user, bd):
    await bd.append_users_item(user)

async def updateUser(user, bd):
    id = user['id']
    for x in user.keys():
        await bd.update_column_by_id(x, 'users', user[x], id)

async def isAdmin(id, bd):
    return await bd.isAdminById(id)

async def isState(id, line, bd):
    if await bd.get_column_by_id('state', 'users', id) == line:
        return True
    else:
        return False

async def setState(id, line, bd):
    await bd.update_column_by_id('state', 'users', line, id)

async def getState(id, bd):
    return await bd.get_column_by_id('state', 'users', id)

async def isAccess(id, bd):
    return await bd.isAccessById(id)

async def setAccess(id, b, bd):
    await bd.update_column_by_id('access', 'users', b, id)

def isCorrectUsers(path):
    schema = {
        123: {
            'username': 'username',
            'kitchen': 'kitchen',
            'area': 'area',
            'access': False,
            'admin': False,
            'state': 'main',
            'favorites': ['favorites']
        }
    }

    try:
        count = 0
        data = getJsonDataWithIntKeys(path)
        validate(data, schema)
        keys = data.keys()
        for x in keys:
            if data[x]["admin"] == True:
                count += 1
            l = list(data[x].keys())
            if len(l) != 7:
                return f"Неверное количество свойств у '{x}'"
            elif data[x]["admin"] == True and data[x]["access"] == False:
                return f"Администратор не может быть без прав доступа к основному ресурсу ('{x}')"
            else:
                for y in l:
                    if y not in ["username", "kitchen", "area", "access", "admin", "state", "favorites"]:
                        return f"Неверное свойство '{y}' у '{x}'"
    except Exception as e:
        print(e)
        return e

    if count == 0:
        return "Необходимо наличие минимум одного Администратора"
    else:
        return ""

async def contentUsersToPath(bd, path):
    data = await getUsers(bd)
    writeJsonData(path, data)

async def contentPathToUsers(path, bd):
    data = getJsonDataWithIntKeys(path)
    users_id = await bd.getAllUsersId()
    new_users_id = list(data.keys())

    for id in new_users_id:
        if id not in users_id:
            newUser = data[id]
            newUser['id'] = id
            await bd.append_users_item(newUser)
        else:
            for x in t_user().keys():
                if x != 'id':
                    if await bd.get_column_by_id(x, 'users', id) != data[id][x]:
                        await bd.update_column_by_id(x, 'users', data[id][x], id)

    for id in users_id:
        if id not in new_users_id:
            await bd.delete_item_by_id('users', id)

async def getSticker(id, bd):
    return await bd.get_column_by_id('telegram_id', 'stickers', id)

async def writeChangesOfRestaurants(bd, rest):
    id = rest['id']

    for x in t_restaurant().keys():
        if x != 'id':
            if await bd.get_column_by_id(x, 'restaurants', id) != rest[x]:
                await bd.update_column_by_id(x, 'restaurants', rest[x], id)

async def writeChangesOfUsers(bd, user):
    id = user['id']

    for x in t_user().keys():
        if x != 'id':
            if await bd.get_column_by_id(x, 'users', id) != user[x]:
                await bd.update_column_by_id(x, 'users', user[x], id)

def getLog(s, text):
    return f"other.py : [{s}] {text}"










