import pymysql as mariadb
import datetime
import sys
import json
sys.path.insert(0, "/home/chris/Community_Manager")

with open("/home/chris/Community_Manager/settings/sql_settings.json") as cfg:
    settings = json.load(cfg)

username     = settings["settings"]["user"]
password     = settings["settings"]["password"]
database     = settings["settings"]["database"]

def get_individual_attendance(family_name):
    mariadb_connection = mariadb.connect(user=username, password=password,database=database)
    cursor = mariadb_connection.cursor()
    query = "SELECT Username, EventName, EventDate FROM GuildList\
    INNER JOIN Attendance ON Attendance.GuildID = %s\
    INNER JOIN EventList ON EventList.EventID = Attendance.EventID;"
    cursor.execute(query, (get_guildID_by_name(family_name)))
    attendance = cursor.fetchall()
    return attendance

def get_full_attendance():
    mariadb_connection = mariadb.connect(user=username, password=password,database=database)
    cursor = mariadb_connection.cursor()
    query = "SELECT Username, EventName, EventDate FROM GuildList\
    INNER JOIN Attendance ON Attendance.GuildID = GuildList.ID\
    INNER JOIN EventList ON EventList.EventID = Attendance.EventID;"
    cursor.execute(query)
    attendance = cursor.fetchall()
    return attendance




def get_guildID_by_name(name):
    mariadb_connection = mariadb.connect(user=username, password=password,database=database)
    cursor = mariadb_connection.cursor()
    sql = "SELECT ID FROM GuildList WHERE Username =%s"
    cursor.execute(sql, (name,))
    guild_id = cursor.fetchone()
    return(guild_id[0])

def get_EventID_by_date(date):
    mariadb_connection = mariadb.connect(user=username, password=password,database=database)
    cursor = mariadb_connection.cursor()
    query = "SELECT EventID FROM EventList WHERE EventDate =(%s)"
    cursor.execute(query, (date, ))
    event_id = cursor.fetchone()
    return event_id[0]

def add_attendance(family_name):
    mariadb_connection = mariadb.connect(user=username, password=password,database=database)
    cursor = mariadb_connection.cursor()
    todaydate = datetime.date.today()
    cursor.execute("SELECT GuildID, EventID FROM Attendance WHERE GuildID = %s AND EventID = %s", (get_guildID_by_name(family_name), get_EventID_by_date(todaydate),))
    data = cursor.fetchone()
    if data == None:
        print("Adding to Attendance List")
        query = "INSERT INTO Attendance (GuildID, EventID) VALUES \
        ((SELECT ID FROM GuildList WHERE Username = %s),\
        (SELECT EventID FROM EventList WHERE EventDate = %s));"
        cursor.execute(query, (family_name, todaydate))
        mariadb_connection.commit()
    else:
        print('Already Added')

def add_today_event(event_name='Nodewar'):
    mariadb_connection = mariadb.connect(user=username, password=password,database=database)
    cursor = mariadb_connection.cursor()
    todaydate = datetime.date.today()
    cursor.execute("SELECT * FROM EventList WHERE EventDate = %s", (todaydate, ))
    data = cursor.fetchone()
    if data == None:
        print("Adding Event")
        query = "INSERT INTO EventList (EventName, EventDate) VALUES (%s, %s)"
        cursor.execute(query, (event_name, todaydate))
        mariadb_connection.commit()



def get_guild_list():
    mariadb_connection = mariadb.connect(user=username, password=password,database=database)
    cursor = mariadb_connection.cursor()
    query = "SELECT Username FROM GuildList"
    cursor.execute(query)
    guild_list = cursor.fetchall()
    return guild_list

def get_full_event():
    mariadb_connection = mariadb.connect(user=username, password=password,database=database)
    cursor = mariadb_connection.cursor()
    query = "SELECT EventDate FROM EventList"
    cursor.execute(query)
    even_list = cursor.fetchall()
    return even_list

