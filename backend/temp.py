import os
import time
import datetime
from urllib2 import urlopen
import json

i = datetime.datetime.now()

#Sends for a JSON file and parses the data into a Database
def read_temp():
    weather_station = '/IE/Cork'
    heating_system_status = False
    key = 'a7e9c74ceafd65c5'
	
    while True:
        #HTTP Request to the Wunderground website returns JSON current conditions
        conditions = urlopen('http://api.wunderground.com/api/{}/geolookup/conditions/q{}.json'.format(key, weather_station))
        conditions_string = conditions.read().decode('utf-8')
        parsed_conditions = json.loads(conditions_string)
	
        #HTTP Request to the Wunderground website returns JSON forecast   
        forecast = urlopen('http://api.wunderground.com/api/{}/forecast/q{}.json'.format(key, weather_station))
        forecast_string = forecast.read().decode('utf-8')
        parsed_forecast = json.loads(forecast_string)
	
        location = parsed_conditions['current_observation']['display_location']['full']
        temp_c = parsed_conditions['current_observation']['feelslike_c']
        windkph = parsed_conditions['current_observation']['wind_kph']
        relative_humidity = parsed_conditions['current_observation']['relative_humidity']
        chance_rain = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['pop']
        high = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['high']['celsius']
        low = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['low']['celsius']
        conditions.close()
        forecast.close()    
        print("recording data into database(period = 5s.)....press ctrl+C to stop!") 	
        time.sleep(10)

if __name__ == "__main__":
    read_temp()