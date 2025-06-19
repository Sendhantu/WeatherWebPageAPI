from collections import defaultdict

from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    if request.method == "POST":
        city = request.form.get("city")
        action = request.form.get("action")

        if action == "Submit":
            return redirect(url_for('weather', city=city))
        elif action == "Tour":
            return redirect(url_for('tripplanner'))
        elif action == "Forecast":
            return redirect(url_for('weatherforcast',city=city))

    return render_template("mainpage.html")


@app.route("/tripplanner")
def tripplanner():
    return render_template("tourplanner.html")


@app.route("/weatherforcast", methods=['GET', 'POST'])
def weatherforcast():
    city_name = request.args.get("city")
    if not city_name:
        return "No city provided", 400

    api_key = "YOUR_API_KEY"
    baseurl = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name, 'appid': api_key, 'units': 'metric'
    }

    response = requests.get(baseurl, params=params)
    forecast_dict = defaultdict(list)

    if response.status_code == 200:
        data = response.json()
        for forecast in data['list'][:5]:
            dt = forecast['dt_txt']
            date, time = dt.split()
            temp = forecast['main']['temp']
            desc = forecast['weather'][0]['description']
            forecast_dict[date].append({'city':city_name,'time': time, 'temp': temp, 'desc': desc})

        return render_template("weatherforecast.html", weather_data=forecast_dict, error=None)
    else:
        error = response.json().get('message', 'Could not fetch forecast')
        return render_template("weatherforecast.html", weather_data=None, error=error)


@app.route("/weather")
def weather():
    city = request.args.get("city")
    if not city:
        return "No city provided", 400

    api_key = "722525c8b51b4d9315b3b8577a599c7e"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S'),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S'),
        }
        return render_template("datadisplay.html", weather=weather, error=None)
    else:
        error = data.get("message", "Unknown error occurred")
        return render_template("datadisplay.html", weather=None, error=error)


if __name__ == "__main__":
    app.run(debug=True)
