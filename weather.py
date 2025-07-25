# weather.py
import requests
import streamlit as st

def get_weather_forecast(city="Cape Town"):
    try:
        api_key = st.secrets["WEATHER_API_KEY"]
        lat, lon = -33.9249, 18.4241
        base_url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "exclude": "current,minutely,hourly,alerts"}
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        tomorrow_data = data["daily"][1]
        min_temp, max_temp = tomorrow_data["temp"]["min"], tomorrow_data["temp"]["max"]
        description = tomorrow_data["weather"][0]["description"]
        rain_chance = tomorrow_data["pop"] * 100 
        
        return (
            f"Tomorrow in {city}, the forecast is a high of {max_temp}°C and a low of {min_temp}°C. "
            f"Expect {description}, with a {rain_chance:.0f}% chance of rain."
        )
    except Exception as e:
        return f"Error: Could not fetch weather data. {e}"