import requests, pycountry
from urllib.parse import quote

api_key = ""

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
    encoded_city = quote(city)
    url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}".format(encoded_city, api_key)
    print(url)
    chord_response = requests.get(url)
    print(chord_response)
    if chord_response == "<Response [200]>":
        print("That is not a valid city")
        start()
    else:
        geo_data = chord_response.json()
        if geo_data == "[]":
            print("That is not a valid city")
            start()
        else:
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]
            return {"lat": lat, "lon": lon}
    

def get_weather(api_key, lat, lon):
    global desc, temp, max_temp, min_temp, humid, wind_speed, country_name, town_name
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    print(url)
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

def start():
    latalon = get_chords(api_key, input("What town do you want weather for? (eg. London, Tokyo, Moscow) "))
    get_weather(api_key, latalon["lat"], latalon["lon"])
    print(f"\nThe weather in {town_name}, {country_name}, is/has {desc}, the current temp is {temp}\N{DEGREE SIGN}C, the maximum temp will be/is {max_temp}\N{DEGREE SIGN}C, and minimum is {min_temp}\N{DEGREE SIGN}C.\nThe current humidity is {humid}%. The current wind speed is {wind_speed}km/h")
    
start()
