import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="rumaan@22",
    database="college_event_management",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = db.cursor()