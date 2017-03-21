import schedule, MySQLdb, sklearn
from time import sleep
from sklearn import tree
import numpy as np

#-------Initialize DB Variables-----------
HOST= "cs1.ucc.ie"
USER = "bdos1"
PASSWD = "ahhuasee"
DB = "2017_bdos1"
#--------/DB Variables-----------------
	
#-------Initialize SciKit Variables--------------
f = open("boiler_training_data.txt")
f.readline()  # skip the header
boiler_data = np.loadtxt(f)
f.close()
x = boiler_data[:, 0:6]  # select columns 1 - 5
y = boiler_data[:, 6:]   # select column 6, the system status
boilerClassifier = tree.DecisionTreeClassifier()
boilerClassifier = boilerClassifier.fit(x, y)

f = open("windows_training_data.txt")
f.readline()  # skip the header
window_data = np.loadtxt(f)
f.close()
x = window_data[:, 0:6]  # select columns 1 - 5
y = window_data[:, 6:]   # select column 6, the system status
windowClassifier = tree.DecisionTreeClassifier()
windowClassifier = windowClassifier.fit(x, y)
#------/intialize SciKit Variables--------------

#------SQL Queries------------------
getTempSQL = "SELECT * FROM interface_temperature ORDER BY time DESC LIMIT 1;"
getWeatherSQL = "SELECT * FROM interface_weather ORDER BY time DESC LIMIT 1;"
getSettingSQL = "SELECT * from interface_user_setting LIMIT 1;"
getHeatingSystemSQL = "SELECT * from interface_heating_system LIMIT 1;"
#-----/ SQL Queries-----------------

#--------------------------------------------------------
#loop to upate whether heating is on/off
#or windows open/closed two system variable
def loop():
    try:
        db = MySQLdb.connect(HOST, USER, PASSWD, DB)        
        cursor = db.cursor()

        temp = fetchOne(cursor, getTempSQL)
        weather = fetchOne(cursor, getWeatherSQL)
        setting = fetchOne(cursor, getSettingSQL)
    
        features= getFeatures(temp, weather)
        boiler = predictBoiler(features)
        windows = predictWindows(features)

        override = setting[3]
        if override == 0:
            cursor.execute("UPDATE interface_heating_system SET status=%s WHERE 1;", (boiler))
            cursor.execute("UPDATE interface_building SET windows=%s WHERE 1;", (windows))
            db.commit()
        db.close()
    except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)

#------------/System Check----------------------

def predictBoiler(features):
    status = boilerClassifier.predict([features])
    return int(round(status[0]))

def predictWindows(features):
    status = windowClassifier.predict([features])
    return int(round(status[0]))

def getFeatures(temp, weather):
    external_c = mapExternalC(temp)
    internal_c = mapInternalC(temp)
    humidity = mapHumidity(weather)
    wind = mapWind(weather)
    expHigh = mapExpHigh(weather)
    expLow = mapExpLow(weather)
    return [external_c, internal_c, humidity, wind, expHigh, expLow]

#----------Fetch One Row from DB---------------
def fetchOne(cursor, sql):
    try:
        cursor.execute(sql)
        return cursor.fetchone()
    except MySQLdb.Error, e:
        return None
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)

#---------/Fetch Row----------------------

#------Maps variables to a range 0-3 (low, medium, high)---------
def mapExternalC(temp):
    external_c = temp[1]
    if external_c > 14: 
        external_c = 2
    elif external_c >= 12:
	    external_c = 1
    else:
        external_c = 0
    return external_c

def mapInternalC(temp):
    internal_c = temp[2]
    if internal_c > 19: 
        internal_c = 2
    elif internal_c >= 17:
	    internal_c = 1
    else:
        internal_c = 0
    return internal_c

def mapHumidity(weather):
    humidity = weather[2]
    if humidity > 60: 
        humidity = 2
    elif humidity >= 50:
	    humidity = 1
    else:
        humidity = 0
    return humidity

def mapWind(weather):
    wind = weather[3]
    if wind > 25: 
         wind = 2
    elif  wind >= 12:
	     wind = 1
    else:
         wind = 0
    return wind

def mapExpHigh(weather):
    high = weather[5]
    if high > 14: 
        high = 2
    elif high >= 12:
	    high = 1
    else:
        high = 0
    return high

def mapExpLow(weather):
    low = weather[6]
    if low > 10: 
        low = 2
    elif low >= 8:
	    low = 1
    else:
        low = 0
    return low
#------/End Maping-----------------------------------------------------------
	
#execute the program
schedule.every(5).seconds.do(loop)
	
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        sleep(1)