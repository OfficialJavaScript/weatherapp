import requests, pycountry
from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import quote
from variables import *
from api_key import api_key

app = Flask(__name__)

@app.route("/")
def index():
    if api_key_error == True or not api_key:
        return render_template("add_api_key.html", api_key=api_key, api_key_error=api_key_error)
    else:
        return render_template("index.html", country=country, town_name=town_name, country_name=country_name, desc=desc, temp=temp, max_temp=max_temp, min_temp=min_temp, humid=humid, wind_speed=wind_speed, error=error)

@app.route("/ask_weather", methods=['POST'])
def query_place():
    global country, desc
    if api_key_error == True or not api_key:
        return render_template("add_api_key.html", api_key=api_key, api_key_error=api_key_error)
    country = request.form.get("town_name")
    latalon = get_chords(api_key, country)
    if error == True:
        return render_template("index.html", country=country, town_name=town_name, country_name=country_name, desc=desc, temp=temp, max_temp=max_temp, min_temp=min_temp, humid=humid, wind_speed=wind_speed, error=error)
    else:
        get_weather(api_key, latalon["lat"], latalon["lon"])
        desc = isorhas(desc)
        return redirect(url_for('index'))

@app.route("/api_key")
def api_key_page():
    return render_template("add_api_key.html", api_key=api_key)

@app.route("/add_api_key", methods=['POST'])
def add_api_key():
    global api_key, api_key, api_key_error
    api_key_error = False
    api_key = request.form.get("api_key")
    if not api_key:
        api_key_error = True
        return render_template("add_api_key.html", api_key=api_key, api_key_error=api_key_error)
    else:
        test_location = quote("London")
        url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}".format(test_location, api_key)
        test_response = requests.get(url)
        if str(test_response.status_code) == "401":
            api_key_error = True
            return render_template("add_api_key.html", api_key=api_key, api_key_error=api_key_error)
        else:
            test_geo_data = test_response.json()
            if 'cod' in test_geo_data and test_geo_data['cod'] == 401 and 'message' in test_geo_data and test_geo_data['message'] == 'Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.':
                api_key_error = True
                return render_template("add_api_key.html", api_key=api_key, api_key_error=api_key_error)
            else:
                return render_template("index.html", country=country, town_name=town_name, country_name=country_name, desc=desc, temp=temp, max_temp=max_temp, min_temp=min_temp, humid=humid, wind_speed=wind_speed, error=error)

def isorhas(desc):
    if desc.lower() == "rain":
        desc = "Rainy"
        return desc
    elif desc.lower() == "sun":
        desc = "Sunny"
        return desc
    elif desc.lower() == "clouds":
        desc = "Cloudy"
        return desc
    elif desc.lower() == "thunder":
        desc = "in a Thunderstorm"
        return desc
    elif desc.lower() == "snow":
        desc = "Snowing"
    elif desc.lower() == "clear":
        desc = "Clear"
    elif desc.lower() == "wind":
        desc = "Windy"
    return desc
    
   
def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country:
            return country.name
        else:
            return "Country not found"
    except Exception as e:
        return str(e)
    
def get_chords(api_key, city):
    global error
    error = False
    encoded_city = quote(city)
    url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}".format(encoded_city, api_key)
    chord_response = requests.get(url)
    if chord_response == "<Response [200]>":
        error = True
    else: 
        geo_data = chord_response.json()
        if not geo_data:
            error = True
        else:
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]
            return {"lat": lat, "lon": lon}

def get_weather(api_key, lat, lon):
    global desc, temp, max_temp, min_temp, humid, wind_speed, country_name, town_name
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    desc = weather_data['weather'][0]['main']
    get_main = weather_data["main"]
    temp = get_main["temp"]
    max_temp = get_main["temp_max"]
    min_temp = get_main["temp_min"]
    humid = get_main["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    country = weather_data["sys"]["country"]
    country_name = get_country_name(country)
    town_name = weather_data["name"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
