from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Weather App</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #74ebd5, #ACB6E5);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 600px;
        }

        .weather-box {
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            text-align: center;
        }

        h1 {
            color: #222;
            margin-bottom: 10px;
            font-size: 32px;
        }

        .subtitle {
            color: #666;
            margin-bottom: 25px;
        }

        form {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
        }

        input {
            flex: 1;
            padding: 14px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            outline: none;
        }

        input:focus {
            border-color: #4a90e2;
        }

        button {
            padding: 14px 22px;
            border: none;
            border-radius: 10px;
            background: #4a90e2;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #357abd;
        }

        .error {
            background: #ffe5e5;
            color: #d60000;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .location {
            margin-bottom: 20px;
        }

        .location h2 {
            color: #222;
            font-size: 26px;
        }

        .location p {
            color: #666;
            margin-top: 5px;
        }

        .temperature {
            font-size: 55px;
            font-weight: bold;
            color: #333;
            margin: 15px 0;
        }

        .condition {
            font-size: 20px;
            color: #555;
            margin-bottom: 25px;
        }

        .weather-details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .detail {
            background: #f5f7fa;
            padding: 18px;
            border-radius: 12px;
        }

        .detail .icon {
            font-size: 25px;
            margin-bottom: 8px;
        }

        .detail h3 {
            color: #333;
            font-size: 16px;
            margin-bottom: 5px;
        }

        .detail p {
            color: #666;
        }

        .footer {
            margin-top: 25px;
            font-size: 13px;
            color: #888;
        }

        @media (max-width: 500px) {
            form {
                flex-direction: column;
            }

            button {
                width: 100%;
            }

            .weather-details {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <div class="weather-box">

        <h1>🌤️ Weather App</h1>

        <p class="subtitle">
            Enter a city to check the current weather
        </p>

        <form method="POST">

            <input
                type="text"
                name="city"
                placeholder="Enter city name..."
                value="{{ city }}"
                required
            >

            <button type="submit">
                Search
            </button>

        </form>


        {% if error %}

            <div class="error">
                ❌ {{ error }}
            </div>

        {% endif %}


        {% if weather %}

            <div class="location">

                <h2>
                    📍 {{ weather.city }}
                </h2>

                <p>
                    {{ weather.country }}
                </p>

            </div>


            <div class="temperature">

                {{ weather.temperature }}°C

            </div>


            <div class="condition">

                ☁️ {{ weather.condition }}

            </div>


            <div class="weather-details">

                <div class="detail">

                    <div class="icon">🌡️</div>

                    <h3>Feels Like</h3>

                    <p>
                        {{ weather.feels_like }}°C
                    </p>

                </div>


                <div class="detail">

                    <div class="icon">💧</div>

                    <h3>Humidity</h3>

                    <p>
                        {{ weather.humidity }}%
                    </p>

                </div>


                <div class="detail">

                    <div class="icon">🌧️</div>

                    <h3>Precipitation</h3>

                    <p>
                        {{ weather.precipitation }} mm
                    </p>

                </div>


                <div class="detail">

                    <div class="icon">💨</div>

                    <h3>Wind Speed</h3>

                    <p>
                        {{ weather.wind_speed }} km/h
                    </p>

                </div>

            </div>


            <div class="footer">

                Last updated: {{ weather.time }}

            </div>

        {% endif %}

    </div>

</div>

</body>
</html>
"""


def get_weather(city):

    # -----------------------------
    # STEP 1: Find city coordinates
    # -----------------------------

    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        geocoding_url,
        params=geocoding_params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data:
        return None

    location = data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    city_name = location["name"]
    country = location.get("country", "Unknown")


    # -----------------------------
    # STEP 2: Get weather
    # -----------------------------

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),

        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    current = weather_data["current"]


    # -----------------------------
    # STEP 3: Weather descriptions
    # -----------------------------

    weather_codes = {

        0: "Clear Sky",

        1: "Mainly Clear",

        2: "Partly Cloudy",

        3: "Overcast",

        45: "Fog",

        48: "Fog",

        51: "Light Drizzle",

        53: "Moderate Drizzle",

        55: "Dense Drizzle",

        61: "Slight Rain",

        63: "Moderate Rain",

        65: "Heavy Rain",

        71: "Slight Snow",

        73: "Moderate Snow",

        75: "Heavy Snow",

        80: "Slight Rain Showers",

        81: "Moderate Rain Showers",

        82: "Heavy Rain Showers",

        95: "Thunderstorm",

        96: "Thunderstorm with Hail",

        99: "Thunderstorm with Heavy Hail"
    }


    condition = weather_codes.get(
        current["weather_code"],
        "Unknown"
    )


    # -----------------------------
    # STEP 4: Return weather data
    # -----------------------------

    return {

        "city": city_name,

        "country": country,

        "temperature": current["temperature_2m"],

        "feels_like": current["apparent_temperature"],

        "humidity": current["relative_humidity_2m"],

        "precipitation": current["precipitation"],

        "wind_speed": current["wind_speed_10m"],

        "condition": condition,

        "time": current["time"]
    }


@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None
    city = ""

    if request.method == "POST":

        city = request.form.get("city", "").strip()

        if not city:

            error = "Please enter a city name."

        else:

            try:

                weather = get_weather(city)

                if weather is None:

                    error = "City not found. Please enter a valid city."

            except requests.exceptions.RequestException:

                error = (
                    "Unable to connect to the weather service. "
                    "Please check your internet connection."
                )

            except Exception as e:

                error = f"Something went wrong: {e}"


    return render_template_string(
        HTML_PAGE,
        weather=weather,
        error=error,
        city=city
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )