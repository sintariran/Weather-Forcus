from flask import Flask, render_template, request
import requests
import logging

app = Flask(__name__)
api_key = "c5a8749c461bc43084610ba776990e83"  # OpenWeatherMapから取得したAPIキーに置き換えてください

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

weather_icons = {
    "01d": "wi-day-sunny",
    "01n": "wi-night-clear",
    "02d": "wi-day-cloudy",
    "02n": "wi-night-cloudy",
    "03d": "wi-cloud",
    "03n": "wi-cloud",
    "04d": "wi-cloudy",
    "04n": "wi-cloudy",
    "09d": "wi-showers",
    "09n": "wi-showers",
    "10d": "wi-day-rain",
    "10n": "wi-night-rain",
    "11d": "wi-thunderstorm",
    "11n": "wi-thunderstorm",
    "13d": "wi-snow",
    "13n": "wi-snow",
    "50d": "wi-fog",
    "50n": "wi-fog"
}

def get_major_cities_weather():
    logging.debug("Fetching weather data for major cities")
    major_cities = ["Tokyo", "Yokohama", "Kyoto", "Osaka", "Sapporo", "Nagoya", "Fukuoka"]
    weather_data = {}

    for city in major_cities:
        logging.debug(f"Fetching weather data for {city}")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data[city] = {
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "temperature": data["main"]["temp"]
            }
        elif response.status_code in [401, 403]:
            logging.error(f"Invalid API key. Failed to fetch weather data for {city}")
        else:
            logging.error(f"Failed to fetch weather data for {city}")
    logging.debug("Completed fetching weather data for major cities")
    return weather_data

@app.route("/", methods=["GET", "POST"])
def index():
    logging.debug("Accessed the main page")
    major_cities = get_major_cities_weather()
    if request.method == "POST":
        city_name = request.form["city"]
        logging.debug(f"Fetching weather data for {city_name}")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code == 200:
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            icon = weather_data["weather"][0]["icon"]
            logging.debug(f"Successfully fetched weather data for {city_name}")
            return render_template("result.html", city=city_name, temperature=temperature, description=description, icon=icon, weather_icons=weather_icons)
        elif response.status_code in [401, 403]:
            error_message = "APIキーが無効です。"
            logging.error(f"Invalid API key. Failed to fetch weather data for {city_name}")
            return render_template("index.html", error=error_message, major_cities=major_cities, weather_icons=weather_icons)
        else:
            error_message = "都市名が見つかりませんでした。"
            logging.error(f"Failed to fetch weather data for {city_name}")
            return render_template("index.html", error=error_message, major_cities=major_cities, weather_icons=weather_icons)

    return render_template("index.html", major_cities=major_cities, weather_icons=weather_icons)

if __name__ == "__main__":
    app.run(debug=True)