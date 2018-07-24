import sys
sys.path.insert(0, "/home/chris/Community_Manager")
import datetime
import asyncio
from tools import sqlmanager


def build_guild_list():
    sql_guild_list = []
    for sql_tuple in sqlmanager.get_guild_list():
        sql_guild_list.append(sql_tuple[0])
    return sql_guild_list


def attendance_helper(event_name, list_of_names):
    sqlmanager.add_today_event(event_name)
    guild_list = build_guild_list()
    for d_name in list_of_names:
        for fam_name in guild_list:
            if fam_name.lower() in d_name.lower():
                print(fam_name)
                sqlmanager.add_attendance(fam_name)

def json_ready_guild_list():
    guild_list = build_guild_list()
    json_ready_gl = []
    for m_name in guild_list:
        json_ready_gl.append({"Name": m_name})
    return json_ready_gl

def get_attendance_list():
    full_guild_attendance = sqlmanager.get_full_attendance()
    formatted_attendance = []
    for attendance_data in full_guild_attendance:
        formatted_attendance.append({"Name":attendance_data[0],"Event Name":attendance_data[1],"Date":str(attendance_data[2])})
    return formatted_attendance

def event_list():
    sql_event_list = sqlmanager.get_full_event()
    formatted_events = []
    for event_data in sql_event_list:
        formatted_events.append({"Date":str(event_data[0])})
    return formatted_events

