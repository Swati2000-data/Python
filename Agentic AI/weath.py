import requests


def get_weather(city):
    # Step 1: Convert city name into latitude and longitude
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(geocoding_url, params=geocoding_params)
    geo_data = geo_response.json()

    # Check if city was found
    if "results" not in geo_data:
        print("❌ City not found. Please enter a valid city name.")
        return

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]
    country = location.get("country", "Unknown")

    # Step 2: Get weather information
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

    weather_response = requests.get(weather_url, params=weather_params)
    weather_data = weather_response.json()

    current = weather_data["current"]

    # Weather code description
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    weather_description = weather_codes.get(
        current["weather_code"],
        "Unknown weather"
    )

    # Step 3: Display weather report
    print("\n" + "=" * 45)
    print(f"🌤️  WEATHER REPORT")
    print("=" * 45)

    print(f"📍 Location       : {city_name}, {country}")
    print(f"🌡️  Temperature    : {current['temperature_2m']} °C")
    print(f"🤒 Feels Like     : {current['apparent_temperature']} °C")
    print(f"💧 Humidity       : {current['relative_humidity_2m']} %")
    print(f"🌧️  Precipitation  : {current['precipitation']} mm")
    print(f"💨 Wind Speed     : {current['wind_speed_10m']} km/h")
    print(f"☁️  Condition      : {weather_description}")
    print(f"🕐 Updated        : {current['time']}")

    print("=" * 45)


# Main program
while True:
    city = input("\nEnter city name (or type 'exit' to quit): ")

    if city.lower() == "exit":
        print("Weather application closed.")
        break

    if city.strip() == "":
        print("Please enter a city name.")
        continue

    try:
        get_weather(city)
    except requests.exceptions.RequestException:
        print("❌ Network error. Please check your internet connection.")
    except Exception as e:
        print(f"❌ Something went wrong: {e}")