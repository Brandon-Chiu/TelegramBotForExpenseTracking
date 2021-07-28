import os
import mysql.connector

my_db = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), passwd=os.getenv('mySQL'), database= os.getenv('database'))

if (my_db):
    print("GOOD!")
else:
    print("FAILED")

mycursor=my_db.cursor()

mycursor.execute("Delete from categories")
my_db.commit()

mycursor.execute("select userId from users")

myResult=mycursor.fetchall()

for i in myResult:
    print(i)

print("done")