import os
import mysql.connector
import datetime

my_db = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), passwd=os.getenv('mySQL'), database= os.getenv('database'))

if (my_db):
    print("GOOD!")
else:
    print("FAILED")

mycursor=my_db.cursor()

mycursor.execute("Delete From users")
my_db.commit()



print("done")