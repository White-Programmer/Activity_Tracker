import json
from datetime import datetime


def manage_name(Activity_Name):
    Name = ["Visual Studio Code", "Chrome", "Chromium", "Python"]
    for i in Name:
        if i in Activity_Name:
            Activity_Name = i
    return Activity_Name


def write_data_to_json(data):
    with open("Activity.json", "w") as f:
        json.dump(data, f, indent=3)


def Activities_in_json():
    Activities = []
    try:
        with open("Activity.json", "r") as f:
            data = json.load(f)
            for i in data["activities"]:
                index = data["activities"].index(i)
                req = data["activities"][index]["name"]
                Activities.append(req)
    except:
        Activities = []
    return Activities


def read_date_from_json(Date, index, Type):
    with open("Activity.json", "r") as f:
        data = json.load(f)
        Req = data["activities"][index]["time"]
        for i in Req:
            if i["date"] == Date:
                if Type == "index":
                    return Req.index(i)
                else:
                    return i["date"]


def get_time_from_json(Activity_Name, Date, Type):
    Activities = Activities_in_json()
    for i in Activities:
        if i == Activity_Name:
            index = Activities.index(i)
            Date_Index = read_date_from_json(Date, index, "index")
            with open("Activity.json", "r") as f:
                Read = json.load(f)
                Req_Time = Read["activities"][index]["time"][Date_Index][Type]
                return Req_Time

def update_no_of_open(index):
    with open("Activity.json", "r") as f:
        data = json.load(f)
        data["activities"][index]["no of open"] = data["activities"][index]["no of open"] + 1
        write_data_to_json(data)

def json_file_manager(Activity_Name, date, end_time, hours, minutes, seconds, start_time):
    Activity_Name = manage_name(Activity_Name)
    data = {"name": Activity_Name, "no of open":1, "time": [{"date": date, "hours": hours,"minutes": minutes, "seconds": seconds, "start_time": start_time, "end_time": end_time}]}
    time = {"date": date, "hours": hours, "minutes": minutes,"seconds": seconds, "start_time": start_time, "end_time": end_time}
    Activities = Activities_in_json()
    if Activities == []:
        data = {"activities": [{"name": Activity_Name,"no of open":1, "time": [{"date": date, "hours": hours,"minutes": minutes, "seconds": seconds, "start_time": start_time, "end_time": end_time}]}]}
        with open("Activity.json", "w") as f:
            json.dump(data, f, indent=3)
    elif Activity_Name in Activities:
        for i in Activities:
            if i == Activity_Name:
                index = Activities.index(i)
        if read_date_from_json(datetime.now().strftime("%d-%m-%Y"), index, "Date") != datetime.now().strftime("%d-%m-%Y"):
            with open("Activity.json", "r") as f:
                Read = json.load(f)
                Read["activities"][index]["time"].append(time)
                write_data_to_json(Read)
                update_no_of_open(index)
                        
        else:
            Hour = get_time_from_json(Activity_Name, datetime.now().strftime("%d-%m-%Y"), "hours")
            Min = get_time_from_json(Activity_Name, datetime.now().strftime("%d-%m-%Y"), "minutes")
            Sec = get_time_from_json(Activity_Name, datetime.now().strftime("%d-%m-%Y"), "seconds")
            time["hours"] = int(time["hours"]) + int(Hour)
            time["seconds"] = (int(time["seconds"]) + int(Sec))%60
            time["minutes"] = (int(time["minutes"]) + int(Min)) + int(time["seconds"])//60
            time["end_time"] = end_time
            if time["minutes"] == 60:
                time["hours"] = int(time["hours"]) + 1
                time["minutes"] = 0
            with open("Activity.json", "r") as f:
                data = json.load(f)
                Date_Index = read_date_from_json(datetime.now().strftime("%d-%m-%Y"), index, "index")
                Req_Time = data["activities"][index]["time"]
                Req_Time[Date_Index] = time
                write_data_to_json(data)
                update_no_of_open(index)
    elif Activity_Name not in Activities:
        with open("Activity.json", "r") as f:
            Read = json.load(f)
            Read["activities"].append(data)
            write_data_to_json(Read)
