import mysql.connector
conn=mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="toor")
if conn.is_connected():
    print("hi")
else:
    print("bye")
