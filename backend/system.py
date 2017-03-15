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

#-------Status Variables-----------
BOILER = 0
WINDOWS = 0
#------/status variables
	
#-------Initialize SciKit Variables--------------
f = open("training_data.txt")
f.readline()  # skip the header
data = np.loadtxt(f)
x = data[:, 0:6]  # select columns 1 - 5
y = data[:, 6:]   # select column 6, the system status
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
print clf.predict([ [2,2,0,0,0,0] ])#Test
#------/intialize SciKit Variables--------------

#------SQL Queries------------------
getTempSQL = "SELECT * FROM interface_temperature ORDER BY time DESC LIMIT 1;"
getWeatherSQL = "SELECT * FROM interface_weather ORDER BY time DESC LIMIT 1;"
getSettingSQL = "SELECT * from interface_user_setting LIMIT 1;"
updateBoilerSQL = "UPDATE interface_heating_system SET status=%s WHERE 1;", (BOILER)
updateWindowsSQL = "UPDATE interface_building SET windows=%s WHERE 1;", (WINDOWS)
#-----/ SQL Queries-----------------

#--------------------------------------------------------
#loop to upate whether heating is on/off
#or windows open/closed two system variable
def loop():
    db = MySQLdb.connect(HOST, USER, PASSWD, DB)        
    cursor = db.cursor()
	
    temp = getTemp(cursor)
    weather = getWeather(cursor)
    setting = getSetting(cursor)
    
    print(mapExternalC(temp))
    override = setting[3]
    if override == 0:
        cursor.execute("UPDATE interface_heating_system SET status=%s WHERE 1;", (BOILER))
        cursor.execute("UPDATE interface_building SET windows=%s WHERE 1;", (WINDOWS))
        db.commit()
        db.close()
    else:
        db.close()
#------------/System Check----------------------

def getTemp(cursor):
    cursor.execute(getTempSQL)
    return cursor.fetchone()

def getWeather(cursor):
    cursor.execute(getWeatherSQL)
    return cursor.fetchone()

def getSetting(cursor):
    cursor.execute(getSettingSQL)
    return cursor.fetchone()

#------Maps External C to a range 0-3 (low, medium, high)---------
def mapExternalC(temp):
    external_c = temp[1]
    if external_c > 14: 
        external_c = 2
    elif external_c >= 12:
	    external_c = 1
    else:
        external_c = 0
    return external_c
#------/End Convert-----------------------------------------------------------

#------Maps Internal C to a range 0-3 (low, medium, high)---------
def mapInternalC(temp):
    internal_c = temp[2]
    if internal_c > 19: 
        internal_c = 2
    elif internal_c >= 17:
	    internal_c = 1
    else:
        internal_c = 0
    return internal_c
#------/End Convert-----------------------------------------------------------

#------Maps humidity to a range 0-3 (low, medium, high)---------
def mapHumidity(weather):
    humidity = weather[2]
    if humidity > 14: 
        humidity = 2
    elif humidity >= 12:
	    humidity = 1
    else:
        humidity = 0
    return humidity
#------/End Convert-----------------------------------------------------------
	
#execute the program
schedule.every(5).seconds.do(loop)
	
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        sleep(1)