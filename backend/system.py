import schedule, MySQLdb, sklearn
from time import sleep
from sklearn import tree
import numpy as np

HOST= "cs1.ucc.ie"
USER = "bdos1"
PASSWD = "ahhuasee"
DB = "2017_bdos1"

f = open("training_data.txt")
f.readline()  # skip the header
data = np.loadtxt(f)
x = data[:, 0:6]  # select columns 1 - 5
y = data[:, 6:]   # select column 6, the system status

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

print clf.predict([ [2,2,0,0,0,0] ])

#loop to upate whether heating is on/off
#or windows open/closed two system variable
def system_check():
    windows = 0
    status = 0
    db = MySQLdb.connect(HOST, USER, PASSWD, DB)        
    cur = db.cursor()
    cur.execute("SELECT * from interface_user_setting")
    user_settings = cur.fetchone()
    override = user_settings[3]
    if override == 0:
        cur.execute("UPDATE interface_heating_system SET status=%s WHERE 1;", (status))
        cur.execute("UPDATE interface_building SET windows=%s WHERE 1;", (windows))
        db.commit()
        db.close()
    else:
        db.close()

#execute the program
schedule.every(5).seconds.do(system_check)
	
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        sleep(1)