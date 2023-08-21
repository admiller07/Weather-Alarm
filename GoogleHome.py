import requests
import schedule
import time
import sys
from datetime import datetime
import pychromecast

API_KEY = 'a1edf70971ebf505b47c4fe45e571b9e'
LAT = '41.8781'
LON = '-87.6298'
URL = f'http://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}'

def get_weather():
    response = requests.get(URL)
    data = response.json()
    current_date = datetime.now().date()
    forecast_details = []
    for forecast in data['list']:
        forecast_date = datetime.fromtimestamp(forecast['dt']).date()
        if forecast_date == current_date:
            weather_description = forecast['weather'][0]['description']
            forecast_time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
            forecast_details.append(f"{forecast_time}: {weather_description.capitalize()}")

    if forecast_details:
        print("Weather forecast for today:")
        for detail in forecast_details:
            print(detail)
    else:
        print("No weather forecast available for today.")

    if any('rain' in detail.lower() for detail in forecast_details):
        return 'Rain'
    else:
        return 'No Rain'

def play_song_on_google_home(song_url):
    chromecasts, _ = pychromecast.get_chromecasts()
    cast = next(cc for cc in chromecasts if cc.name == "Master Bedroom Display")
    cast.wait()
    mc = cast.media_controller
    mc.play_media(song_url, 'audio/mp3')
    mc.block_until_active()

def play_song():
    weather = get_weather()
    if weather == 'Rain':
        song_url = 'https://drive.google.com/uc?export=download&id=1t4HOV8Fq_59N9LJtp9GwJ7Ywv0-Sgf9D'
    else:
        song_url = 'https://drive.google.com/uc?export=download&id=1ojVLwkBRkNP_-MBDVwx8Ep-wBQdVWx_U'

    play_song_on_google_home(song_url)

def alarm():
    print("Alarm triggered!")
    play_song()

# Get the alarm time from the command-line arguments
if len(sys.argv) > 1:
    alarm_time = sys.argv[1]
    print(f"Alarm has been set successfully for {alarm_time}!") # Confirmation message
else:
    print("Please provide the alarm time as a command-line argument (HH:MM).")
    sys.exit(1)

# Schedule the alarm at the specified time
schedule.every().day.at(alarm_time).do(alarm)

while True:
    schedule.run_pending()
    time.sleep(1)
