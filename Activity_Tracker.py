import subprocess
import re
from datetime import datetime
import TimeCalculator
import Json_Activity


def get_active_window_raw():
    root = subprocess.Popen(
        ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()
    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(
            ['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
        value = stdout.decode('utf-8').split("=")[1].replace('"', '')
        if "*" in value:
            value = value.replace("*", "")
        if "\n" in value:
            value = value.replace("\n", "")
        if value[0] == " ":
            value = value[1:]
        return value

if __name__ == "__main__":
    active_window = ""
    Start_Time = datetime.now().strftime("%H:%M:%S")
    time = True
    with open("WindowLog", "a") as f:
        f.write("\t\t\t\t\t" + datetime.now().strftime("%d-%m-%Y") + "\n")
    while 1:
        try:
            new_window_name = get_active_window_raw()
            if active_window != new_window_name:
                print(new_window_name)
                with open("WindowLog", "r") as f:
                    read = f.readlines()
                    if read[-1] != new_window_name:
                        with open("WindowLog", "a") as f:
                            f.write(new_window_name + "\n")
                if not time:
                    End_Time = datetime.now().strftime("%H:%M:%S")
                    Start, End, Hour, Min, Sec, Date = TimeCalculator.time_calculator(
                        Start_Time, End_Time)
                    Json_Activity.json_file_manager(active_window, datetime.now().strftime("%d-%m-%Y"), End, Hour, Min, Sec, Start)
                    Start_Time = datetime.now().strftime("%H:%M:%S")
            active_window = new_window_name
            time = False

        except Exception as e:
    ##        print("Error-: " + str(e))
    ##        break
            if new_window_name != 'Desktop':
                new_window_name = 'Desktop'
                with open("WindowLog", "a") as f:
                    f.write("Desktop\n")
                continue
