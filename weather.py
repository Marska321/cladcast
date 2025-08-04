# weather.py

import requests
import streamlit as st

def get_weather_forecast(city="Cape Town"):
    """
    Fetches the NEXT DAY weather forecast using the WeatherAPI.com service.
    """
    try:
        api_key = st.secrets["WEATHER_API_KEY"]
        
        # --- The API endpoint for WeatherAPI.com ---
        base_url = "http://api.weatherapi.com/v1/forecast.json"
        
        # --- The parameters have changed ---
        # We request 2 days to ensure we get tomorrow's forecast
        params = {
            "key": api_key,
            "q": city,
            "days": 2 
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # --- We now parse the new JSON structure for tomorrow's forecast ---
        # The 'forecastday' list contains forecasts. Today is at index 0, tomorrow is at index 1.
        tomorrow_data = data["forecast"]["forecastday"][1]
        
        day_info = tomorrow_data["day"]
        min_temp = day_info["mintemp_c"]
        max_temp = day_info["maxtemp_c"]
        description = day_info["condition"]["text"]
        rain_chance = day_info["daily_chance_of_rain"]
        
        formatted_weather = (
            f"Tomorrow in {city}, the forecast is a high of {max_temp}°C and a low of {min_temp}°C. "
            f"Expect {description}, with a {rain_chance}% chance of rain."
        )
        return formatted_weather
        
    except requests.exceptions.RequestException as e:
        return f"Error: Could not fetch weather data. {e}"
    except (KeyError, IndexError):
        return "Error: Weather data format from WeatherAPI.com is unexpected or incomplete."
