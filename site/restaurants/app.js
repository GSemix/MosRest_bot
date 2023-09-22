let tg = window.Telegram.WebApp;
url = new URL(window.location.href);

var choise = {
        "type": "rest",
        "restaurant": ""
}

type_page = url.searchParams.get('type_page');

async function get_restaurants() {
    if (type_page == 'location') {
        latitude = url.searchParams.get('latitude');
        longitude = url.searchParams.get('longitude');
        fetchs_url = 'https://digitalplatforms.su/api_mos_rest/get_restaurants_by_location/' + latitude + '/' + longitude
    } else if (type_page == 'params') {
        kitchen = url.searchParams.get('kitchen');
        area = url.searchParams.get('area');
        fetchs_url = 'https://digitalplatforms.su/api_mos_rest/get_restaurants_by_params/' + kitchen + '/' + area
    } else if (type_page == 'search') {
        text = url.searchParams.get('text');
        fetchs_url = 'https://digitalplatforms.su/api_mos_rest/get_restaurants_by_name/' + text
    } else if (type_page == 'favorites') {
        id = url.searchParams.get('id');
        fetchs_url = 'https://digitalplatforms.su/api_mos_rest/get_restaurants_favorites/' + id
    } else if (type_page == 'selections') {
        selection_id = url.searchParams.get('id');
        fetchs_url = 'https://digitalplatforms.su/api_mos_rest/get_restaurants_selections/' + selection_id
    } else if (type_page == 'top') {
        fetchs_url = 'https://digitalplatforms.su/api_mos_rest/get_restaurants_top'
    }

    await fetch(fetchs_url)
    .then((data) => {
        return data.json()
    })
    .then(response => {
                if (document.getElementById("restaurants")) {
                    document.getElementById("restaurants").innerHTML = response['data'];
                }
    })
}

function choise_restaurant(item_name) {
    choise['restaurant'] = item_name
    tg.sendData(JSON.stringify(choise));
};

window.onload = function() {
    get_restaurants()
}

var minValue = 700; // Начальное значение первого ползунка
var maxValue = 7000; // Начальное значение второго ползунка

$(function() {
    var ct = [minValue, 1000, 2000, 2500, 3000, maxValue]
  var slider = $("#slider-range").slider({
    range: true,
    min: 100,
    max: 7000,
    values: [minValue, maxValue],
    slide: function(event, ui) {
      var closestValue = getClosestValue(ui.value, controlPoints);
      ui.value = closestValue;
      updateAmount(ui.values);
    }
  });

  function getClosestValue(value, arr) {
    return arr.reduce(function(prev, curr) {
      return (Math.abs(curr - value) < Math.abs(prev - value) ? curr : prev);
    });
  }

  updateAmount(slider.slider("values"));
});
