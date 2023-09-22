#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Запуска  ->  uvicorn --host 127.0.0.1 --port 3100 api:app --workers 1

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio

from file import getJsonData
from file import get_areas_json
from file import get_kitchens_json
from db import BD
from db import params
from other import isInt
from other import isFloat

bd = BD(params)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])   # Добавляем CORS-мидлвэр для обработки CORS-заголовков

itude_zone = 0.02
itude_zone_max = 0.2

@app.on_event("startup")
async def startup_event():
    await bd.create_pool()
    await bd.check_tables()

@app.on_event("shutdown")
async def shutdown_event():
    await bd.close_pool()

# curl http://127.0.0.1:3100/api_mos_rest/hello
@app.get("/api_mos_rest/hello")
async def hello(request: Request):
    return {"data": "Hello, World!"}

# curl http://127.0.0.1:3100/api_mos_rest/get_kitchens
@app.route('/api_mos_rest/get_kitchens', methods=['GET'])
def get_kitchens(request: Request):
    kitchens = get_kitchens_json()
    data = ""

    for x in kitchens.keys():
        data += f"""
<div class="card" id="{kitchens[x]['card_name']}" onclick="choise_kitchen('{kitchens[x]['card_name']}');">
    <span class="card-description">{kitchens[x]['name']}</span>
</div>
<style type="text/css">
    #{kitchens[x]['card_name']} {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{kitchens[x]['image']}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        border: 2px solid #000000;
    }}
</style>
"""

    response = {"data": data}

    return JSONResponse(content=response)

# curl http://127.0.0.1:3100/api_mos_rest/get_areas
@app.route('/api_mos_rest/get_areas', methods=['GET'])
def get_areas(request: Request):
    areas = get_areas_json()
    data = ""

    for x in areas.keys():
        data += f"""
<div class="card" id="{areas[x]['card_name']}" onclick="choise_area('{areas[x]['card_name']}');">
    <span class="card-description">{areas[x]['name']}</span>
</div>
<style type="text/css">
    #{areas[x]['card_name']} {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{areas[x]['image']}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        border: 2px solid #000000;
    }}
</style>
"""

    response = {"data": data}

    return JSONResponse(content=response)

# curl http://127.0.0.1:3100/api_mos_rest/get_restaurants_by_location/55.549443/37.700694
@app.route('/api_mos_rest/get_restaurants_by_location/{latitude}/{longitude}', methods=['GET'])
async def get_restaurants_by_location(request: Request):
    data = ""
    latitude = request.path_params['latitude']
    longitude = request.path_params['longitude']

    if isFloat(latitude) and isFloat(longitude):
        restaurants = await bd.getRestaurantsLocation()
        result = []

        if restaurants != []:
            user_latitude = float(latitude)
            user_longitude = float(longitude)
            text_content = ""
            local_itude_zone = itude_zone

            while result == [] and local_itude_zone <= itude_zone_max:
                for x in restaurants:
                    try:
                        latitude = x['latitude']
                        longitude = x['longitude']

                        if (latitude < user_latitude + local_itude_zone and latitude >= user_latitude - local_itude_zone) and (longitude < user_longitude + local_itude_zone and longitude >= user_longitude - local_itude_zone):
                            if x not in result:
                                result.append(x)
                    except Exception as e:
                            pass
                local_itude_zone += 0.0001

            if result != []:
                for x in result:
                    if x['image'] == "":
                        x['image'] = "../media/photo.jpg"
                    data += f"""
    <div class="card" id="r-card-{x['id']}" onclick="choise_restaurant('r-card-{x['id']}');">
        <div class="card-description">
            <span class="card-description">{x['name']}</span>
            <hr style="border: 0.1px solid white;">
            <span class="card-description thin-font">{x['address']}</span>
        </div> 
    </div>
    <style type="text/css">
        #r-card-{x['id']} {{
            background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{x['image']}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
        }}
    </style>
    """
            else:
                data = '<h3 align="center" style="color:White;">😥 Рядом ничего нет<h3>'
        else:
            data = '<h3 align="center" style="color:White;">😥 Рядом ничего нет<h3>'
    else:
        data = '<h3 align="center" style="color:White;">😳 Произошла какая-то ошибка<h3>'

    response = {"data": data}

    return JSONResponse(content=response)

# curl http://127.0.0.1:3100/api_mos_rest/get_restaurants_top
@app.route('/api_mos_rest/get_restaurants_top', methods=['GET'])
async def get_restaurants_top(request: Request):
    data = ""
    counter = 1
    restaurants = await bd.getTop10Restaurant()

    if restaurants != []:
        for x in restaurants:
            if x['image'] == "":
                x['image'] = "../media/photo.jpg"
            data += f"""
<div class="card" id="r-card-{x['id']}" onclick="choise_restaurant('r-card-{x['id']}');">
        <div class="card-description">
            <span class="card-description">{counter}. {x['name']}({x['score']})</span>
            <hr style="border: 0.1px solid white;">
            <span class="card-description thin-font">{x['address']}</span>
        </div>
</div>
<style type="text/css">
    #r-card-{x['id']} {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{x['image']}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        {"border: 3px solid #FFD700;" if counter == 1 else ""}
        {"border: 3px solid #C0C0C0;" if counter == 2 else ""}
        {"border: 3px solid #CD7F32;" if counter == 3 else ""}
    }}
</style>
"""
            counter += 1
    else:
        data = '<h3 align="center" style="color:White;">😥 Пока ничего нет<h3>'

    response = {"data": data}

    return JSONResponse(content=response)

# curl http://127.0.0.1:3100/api_mos_rest/get_restaurants_selections/1
@app.route('/api_mos_rest/get_restaurants_selections/{selection_id}', methods=['GET'])
async def get_restaurants_selections(request: Request):
    data = ""
    selection_id = int(request.path_params['selection_id'])
    selection = await bd.getSelectionById(selection_id)

    if selection:
        if selection['type_selection'] == 'restaurants_top_10':
            restaurants = [await bd.getRestaurantById(rest_id) for rest_id in selection['id_list']]
            counter = 1

            if restaurants != []:
                for x in restaurants:
                    if x['image'] == "":
                        x['image'] = "../media/photo.jpg"
                    data += f"""
    <div class="card" id="r-card-{x['id']}" onclick="choise_restaurant('r-card-{x['id']}');">
        <div class="card-description">
            <span class="card-description">{counter}. {x['name']}</span>
            <hr style="border: 0.1px solid white;">
            <span class="card-description thin-font">{x['address']}</span>
        </div>
    </div>
    <style type="text/css">
        #r-card-{x['id']} {{
            background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{x['image']}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
            {"border: 3px solid #FFD700;" if counter == 1 else ""}
            {"border: 3px solid #C0C0C0;" if counter == 2 else ""}
            {"border: 3px solid #CD7F32;" if counter == 3 else ""}
        }}
    </style>
    """
                    counter += 1
            else:
                data = '<h3 align="center" style="color:White;">😥 Пока ничего нет<h3>'
        elif selection['type_selection'] == 'restaurants_list':
            restaurants = [await bd.getRestaurantById(rest_id) for rest_id in selection['id_list']]

            if restaurants != []:
                for x in restaurants:
                    if x['image'] == "":
                        x['image'] = "../media/photo.jpg"
                    data += f"""
    <div class="card" id="r-card-{x['id']}" onclick="choise_restaurant('r-card-{x['id']}');">
        <div class="card-description">
            <span class="card-description">{x['name']}</span>
            <hr style="border: 0.1px solid white;">
            <span class="card-description thin-font">{x['address']}</span>
        </div>
    </div>
    <style type="text/css">
        #r-card-{x['id']} {{
            background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{x['image']}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
        }}
    </style>
    """
            else:
                data = '<h3 align="center" style="color:White;">😥 Пока ничего нет<h3>'
        else:
            data = '<h3 align="center" style="color:White;">😥 Подборка не найдена<h3>'
    else:
        data = '<h3 align="center" style="color:White;">😥 Подборка не найдена<h3>'

    response = {"data": data}

    return JSONResponse(content=response)

# curl http://127.0.0.1:3100/api_mos_rest/get_restaurants_favorites/490483818
@app.route('/api_mos_rest/get_restaurants_favorites/{id}', methods=['GET'])
async def get_restaurants_favorites(request: Request):
    id = request.path_params['id']
    data = ""

    if isInt(id):
        id = int(id)
        user = await bd.getUserById(id)
        favorites = []

        for x in user['favorites']:
            favorites.append(await bd.getRestaurantById(int(x)))

        if favorites != []:
            for x in favorites:
                if x['image'] == "":
                    x['image'] = "../media/photo.jpg"
                data += f"""
    <div class="card" id="r-card-{x['id']}" onclick="choise_restaurant('r-card-{x['id']}');">
        <div class="card-description">
            <span class="card-description">{x['name']}</span>
            <hr style="border: 0.1px solid white;">
            <span class="card-description thin-font">{x['address']}</span>
        </div>
    </div>
    <style type="text/css">
        #r-card-{x['id']} {{
            background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{x['image']}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
        }}
    </style>
    """
        else:
            data = '<h3 align="center" style="color:White;">😥 Пока ничего нет<h3>'
    else:
        data = '<h3 align="center" style="color:White;">😳 Произошла какая-то ошибка<h3>'

    response = {"data": data}

    return JSONResponse(content=response)

# curl http://127.0.0.1:3100/api_mos_rest/get_restaurants_by_name/ar
@app.route('/api_mos_rest/get_restaurants_by_name/{text}', methods=['GET'])
async def get_restaurants_by_name(request: Request):
    data = ""
    text = request.path_params['text']

    (main_restaurants, mb_restaurants) = await bd.getRestaurantsByName(text)

    if main_restaurants != []:
        for x in main_restaurants:
            if x['image'] == "":
                x['image'] = "../media/photo.jpg"
            data += f"""
<div class="card" id="r-card-{x['id']}" onclick="choise_restaurant('r-card-{x['id']}');">
        <div class="card-description">
            <span class="card-description">{x['name']}</span>
            <hr style="border: 0.1px solid white;">
            <span class="card-description thin-font">{x['address']}</span>
        </div>  
</div>
<style type="text/css">
    #r-card-{x['id']} {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{x['image']}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }}
</style>
"""
    else:
        data = '<h3 align="center" style="color:White;">😥 Такого нет<h3>'

    if mb_restaurants != []:
        data += '\n<h3 style="color:White;">Возможно имели ввиду:</h3>\n'

        for x in mb_restaurants:
            if x['image'] == "":
                x['image'] = "../media/photo.jpg"
            data += f"""
<div class="card" id="r-card-{x['id']}" onclick="choise_restaurant('r-card-{x['id']}');">
        <div class="card-description">
            <span class="card-description">{x['name']}</span>
            <hr style="border: 0.1px solid white;">
            <span class="card-description thin-font">{x['address']}</span>
        </div>
</div>
<style type="text/css">
    #r-card-{x['id']} {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{x['image']}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }}
</style>
"""

    response = {"data": data}

    return JSONResponse(content=response)

# Авторская + Любой
# curl http://127.0.0.1:3100/api_mos_rest/get_restaurants_by_params/%D0%90%D0%B2%D1%82%D0%BE%D1%80%D1%81%D0%BA%D0%B0%D1%8F/%D0%9B%D1%8E%D0%B1%D0%BE%D0%B9
@app.route('/api_mos_rest/get_restaurants_by_params/{kitchen}/{area}', methods=['GET'])
async def get_restaurants_by_params(request: Request):
    kitchen = request.path_params['kitchen']
    area = request.path_params['area']
    kitchens = get_kitchens_json()
    areas = get_areas_json()
    data = ""

    restaurants = await bd.getRestaurantsByKitchenAndArea(kitchen, area)

    for x in restaurants:
        if x['image'] == "":
            x['image'] = "../media/photo.jpg"
        data += f"""
<div class="card" id="r-card-{x['id']}" onclick="choise_restaurant('r-card-{x['id']}');">
        <div class="card-description">
            <span class="card-description">{x['name']}</span>
            <hr style="border: 0.1px solid white;">
            <span class="card-description thin-font">{x['address']}</span>
        </div>
</div>
<style type="text/css">
    #r-card-{x['id']} {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{x['image']}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }}
</style>
"""

    response = {"data": data}

    return JSONResponse(content=response)

# Авторская
# curl http://127.0.0.1:3100/api_mos_rest/get_available_areas/%D0%90%D0%B2%D1%82%D0%BE%D1%80%D1%81%D0%BA%D0%B0%D1%8F
@app.route('/api_mos_rest/get_available_areas/{kitchen}', methods=['GET'])
async def get_available_areas(request: Request):
    kitchens = get_kitchens_json()
    card_name = request.path_params['kitchen']
    kitchen = ""

    for x in kitchens:
        if kitchens[x]["card_name"] == card_name:
            kitchen = kitchens[x]["name"]

    areas = get_areas_json()
    available_areas = await bd.getAreasByKitchen(kitchen)
    areas_keys = list(areas.keys())
    data = ""

    for x in areas_keys:
        if areas[x]['name'] not in available_areas:
            if areas[x]['name'] != "Любой":
                areas.pop(x)

    for x in areas.keys():
        data += f"""
<div class="card" id="{areas[x]['card_name']}" onclick="choise_area('{areas[x]['card_name']}');">
    <span class="card-description">{areas[x]['name']}</span>
</div>
<style type="text/css">
    #{areas[x]['card_name']} {{
        background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.75), rgba(0,0,0,0.25)), url("{areas[x]['image']}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        border: 2px solid #000000;
    }}
</style>
"""

    response = {"data": data}

    return JSONResponse(content=response)







