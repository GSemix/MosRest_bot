def t_user():
    return {
        'id': 0,
        'username': 'username',
        'kitchen': '',
        'area': '',
        'access': True,
        'admin': False,
        'state': 'main',
        'favorites': []
    }

def t_restaurant():
    return {
        "id": 0,
        "name": "name",
        "image": "images/image.jpg",
        "url_map": "url_map",
        "url_site": "url_site",
        "url_menu": "url_menu",
        "address": "address",
        "area": "area",
        "kitchen": [
            "kitchen"
        ],
        "description": "description",
        "lat_longitude": "lat, longitude",
        "favorites": [
            "1",
            "2",
            "3"
        ],
        "average_check": 123,
        "social_media": '{"name":"url"}'
    }
