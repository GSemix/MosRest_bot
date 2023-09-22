let tg = window.Telegram.WebApp;
var main_button = document.querySelector("#main-button")
var areas_description = document.querySelector("#areas-description")

var choise = {
        "type": "params",
        "kitchen": "",
        "area": ""
}

function choise_kitchen(item_name) {
        let current_element = document.getElementById(choise["kitchen"])

        if (current_element) {
                current_element.style = 'border: 2px solid #000000;';
        }

        document.getElementById(item_name).style = 'border: 2px solid #4CAF50;';
        main_button.style.display = 'inline-block';
	areas_description.style.display = 'none';
	choise["kitchen"] = item_name;
        get_available_areas();
        choise["area"] = "";
};

function choise_area(item_name) {
        let current_element = document.getElementById(choise["area"])

        if (current_element) {
                current_element.style = 'border: 2px solid #000000;';
        }

        document.getElementById(item_name).style = 'border: 2px solid #4CAF50;';
        choise["area"] = item_name;
};

async function get_kitchens() {
    await fetch('https://digitalplatforms.su/api_mos_rest/get_kitchens')
    .then((data) => {
        return data.json()
    })
    .then(response => {
                if (document.getElementById("kitchens")) {
                        document.getElementById("kitchens").innerHTML = response['data'];
                }
    })
}

async function get_areas() {
    await fetch('https://digitalplatforms.su/api_mos_rest/get_areas')
    .then((data) => {
        return data.json()
    })
    .then(response => {
                if (document.getElementById("areas")) {
                        document.getElementById("areas").innerHTML = response['data'];
                }
    })
}

// http://127.0.0.1:5000/get_available_areas/
async function get_available_areas() {
    await fetch('https://digitalplatforms.su/api_mos_rest/get_available_areas/' + choise["kitchen"])
    .then((data) => {
        return data.json()
    })
    .then(response => {
                if (document.getElementById("areas")) {
                        document.getElementById("areas").innerHTML = response['data'];
                }
    })
}

window.onload = function() {
        main_button.style.display = 'none';
        get_kitchens()
        //get_areas()
}

main_button.addEventListener("click", function() {
        if (choise['kitchen'] == "") {
                alert('Выберите кухню')
        } else if (choise['area'] == "") {
                alert('Выберите район')
        } else {
                tg.sendData(JSON.stringify(choise));

                // file:///Users/sm/Desktop/Projects/My/Telegram/mos_rest/site/test/index.html?kitchen=
                //location.href = 'https://digitalplatforms.su/mos_rest_restaurants?kitchen=' + choise['kitchen'] + '&area=' + choise['area'];
        }
});












