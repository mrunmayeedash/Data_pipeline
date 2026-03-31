import pymysql
connector=pymysql.connect(
    user="root",
    host="localhost",
    password="123456789",
    port=3306)
print(connector,"connection succesful Go aheed")