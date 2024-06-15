import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import matplotlib.pyplot as plt

def setup_openmeteo_client():
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)

def fetch_weather_data(client, latitude, longitude, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "precipitation"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "precipitation_sum"],
        "timezone": "Europe/London"
    }
    return client.weather_api(url, params=params)

def process_hourly_data(hourly):
    data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "precipitation": hourly.Variables(1).ValuesAsNumpy()
    }
    return pd.DataFrame(data)

def process_daily_data(daily):
    data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s"),
            end=pd.to_datetime(daily.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),
        "temperature_2m_min": daily.Variables(1).ValuesAsNumpy(),
        "temperature_2m_mean": daily.Variables(2).ValuesAsNumpy(),
        "precipitation_sum": daily.Variables(3).ValuesAsNumpy()
    }
    return pd.DataFrame(data)

def visualize_hourly_data(hourly_dataframe):
    plt.figure(figsize=(12, 6))
    plt.plot(hourly_dataframe['date'], hourly_dataframe['temperature_2m'], label='Temperature (2m)')
    plt.plot(hourly_dataframe['date'], hourly_dataframe['precipitation'], label='Precipitation')
    plt.title('Hourly Weather Data')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)
    plt.show()

def visualize_daily_data(daily_dataframe):
    plt.figure(figsize=(12, 6))
    plt.plot(daily_dataframe['date'], daily_dataframe['temperature_2m_max'], label='Max Temperature (2m)')
    plt.plot(daily_dataframe['date'], daily_dataframe['temperature_2m_min'], label='Min Temperature (2m)')
    plt.plot(daily_dataframe['date'], daily_dataframe['temperature_2m_mean'], label='Mean Temperature (2m)')
    plt.plot(daily_dataframe['date'], daily_dataframe['precipitation_sum'], label='Precipitation Sum')
    plt.title('Daily Weather Data')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    openmeteo_client = setup_openmeteo_client()

    # Replace these coordinates and date range with the desired values
    latitude = 52.52
    longitude = 13.41
    start_date = "2023-12-16"
    end_date = "2023-12-30"

    weather_responses = fetch_weather_data(openmeteo_client, latitude, longitude, start_date, end_date)

    for response in weather_responses:
        print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        hourly_dataframe = process_hourly_data(response.Hourly())
        print(hourly_dataframe)

        daily_dataframe = process_daily_data(response.Daily())
        print(daily_dataframe)

        visualize_hourly_data(hourly_dataframe)
        visualize_daily_data(daily_dataframe)
