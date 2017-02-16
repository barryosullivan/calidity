import os
import time
import glob
from urllib2 import urlopen
import json

os.system('modprobe w1-gpio')                              # load one wire communication device kernel modules
os.system('modprobe w1-therm')                                                 
base_dir = '/sys/bus/w1/devices/'                          # point to the address
device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from 28*
device_file = device_folder + '/w1_slave'                  # store the details

def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()                                   # read the device details
   f.close()
   return lines

#Sends for a JSON file and parses the data into a Database
def read_temp():
    weather_station = '/IE/Cork'
    heating_system_status = False
    key = 'a7e9c74ceafd65c5'
	
    while True:
	    # GET EXTERNAL DATA FIRST
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
		
		#GET INTERNAL DATA NEXT
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':                   # ignore first line
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')                        # find temperature in the details
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0                 # convert to Celsius
            print(temp_c)		

if __name__ == "__main__":
    read_temp()
    time.sleep(10)