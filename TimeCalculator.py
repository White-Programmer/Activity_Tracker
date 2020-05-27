from datetime import datetime

def time_calculator(start, end):
    date = datetime.now().strftime("%d-%m-%Y")
    Start_Time = start.split(":")
    End_Time = end.split(":")
    total_end_sec = int(End_Time[0])*(60*60) + int(End_Time[1])*60 + int(End_Time[2])
    total_start_sec = int(Start_Time[0])*(60*60) + int(Start_Time[1])*60 + int(Start_Time[2])
    Minus = total_end_sec - total_start_sec
    if Minus < 0 :
        Minus = Minus*(-1)
    Hour = Minus//(60*60)
    Min = Minus//60
    if Min == 60:
        Min = 0
    Second = Minus%60
    return str(Start_Time), str(End_Time), str(Hour), str(Min), str(Second), date
