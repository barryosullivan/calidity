import os, time, glob, json, MySQLdb, schedule
from urllib2 import urlopen
from datetime import datetime

os.system('modprobe w1-gpio')                             
os.system('modprobe w1-therm')                                                 
base_dir = '/sys/bus/w1/devices/'                         
device_folder = glob.glob(base_dir + '28*')[0]      
device_file = device_folder + '/w1_slave'              

#Keys for wunderground website
weather_station = '/IE/Cork'
key = 'a7e9c74ceafd65c5'

#read the raw temperature data from sensor
def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()                                 
   f.close()
   return lines

#reads External & Internal temps in degrees Celcius
def read_temp():
	#===========GET EXTERNAL TEMP FIRST=====================
	#HTTP Request to the Wunderground website returns JSON current conditions
	conditions = urlopen('http://api.wunderground.com/api/{}/geolookup/conditions/q{}.json'.format(key, weather_station))
	conditions_string = conditions.read().decode('utf-8')
	parsed_conditions = json.loads(conditions_string)

	time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	external_c = parsed_conditions['current_observation']['temp_c']
	
	conditions.close()
	
	#=========GET INTERNAL TEMP NEXT================================
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':                
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')                        
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		internal_c = float(temp_string) / 1000.0               
	
	db = MySQLdb.connect(host="cs1.ucc.ie",   
					user="bdos1",         
					passwd="ahhuasee",  
					db="2017_bdos1")        

	cur = db.cursor()
	cur.execute("INSERT INTO interface_temperature (time, external_c, internal_c) VALUES (%s, %s, %s);", (time_now, external_c, internal_c))
	db.commit()
	db.close()

#Fetches the latest weather forecast for the day
def read_weather():
	#HTTP Request to the Wunderground website returns JSON forecast   
	forecast = urlopen('http://api.wunderground.com/api/{}/forecast/q{}.json'.format(key, weather_station))
	forecast_string = forecast.read().decode('utf-8')
	parsed_forecast = json.loads(forecast_string)

	time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	conditions = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['conditions']
	humidity = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['avehumidity']
	wind_kph = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['avewind']['kph']
	chance_rain = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['pop']
	high = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['high']['celsius']
	low = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['low']['celsius']
	snow = parsed_forecast['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['in']
	
	db = MySQLdb.connect(host="cs1.ucc.ie",   
					user="bdos1",         
					passwd="ahhuasee",  
					db="2017_bdos1")        

	cur = db.cursor()
	cur.execute("INSERT INTO interface_weather (time, conditions, humidity, wind_kph, chance_rain, high, low, snow) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (time_now, conditions, humidity, wind_kph, chance_rain, high, low, snow))
	db.commit()
	db.close()

#execute the program
schedule.every(15).minutes.do(read_temp)
schedule.every(6).hours.do(read_weather)
	
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)