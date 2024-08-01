## 
import datetime
import time
import pcdr
from pcdr.unstable.flow import OsmoSingleFreqReceiver
import os
from playsound import playsound
 
cent_freq = int(input("Enter center frequency is hz.: "))

def safePlay(fn, block):
    try:
        playsound(fn, '/home/michael.j.e.holloway58/Desktop/Holloway_file')
    except Exception:
        print("Failed to play the sound.")
 
 
rec = OsmoSingleFreqReceiver("hackrf=0", (cent_freq))
rec.start()
short_avg = 0
long_avg = 5  # Arbitrary; adjust to taste
count = 0
start_time = time.time()
fn = "activity.csv"
if os.path.exists(fn):
    newfile = False
else:
    newfile = True
with open(fn, "a", encoding="utf-8") as f:
    if newfile:
        f.write("passedThresh,date,time,unix_timestamp,time_since_start,strength,short_avg,long_avg\n")
    
    while True:
        stren = rec.get_strength()
        short_avg = 0.9*short_avg + 0.1*stren
        long_avg = 0.9999*long_avg + 0.0001*stren
        count += 1
        if count == 100:  # Record every hundredth
            count = 0
 
            nowtime = time.time()
            timedelta = nowtime - start_time
            dt = datetime.datetime.fromtimestamp(nowtime)
#            print(f"{dt}  Recording to file.")
 
            if short_avg > 1.2 * long_avg:
                safePlay("Bell.wav", block=False)
                print(f"BIG SPIKE {nowtime}")
                f.write("BIG SPIKE,")
                f.write(f"{dt.date()},{dt.time()},{nowtime},{timedelta},{stren},{short_avg},{long_avg}\n")
                f.flush()
            elif short_avg > 1.1 * long_avg:
                safePlay("Buzzer.wav", block=False)
                print("SPIKE")
                f.write("SPIKE,")
                f.write(f"{dt.date()},{dt.time()},{nowtime},{timedelta},{stren},{short_avg},{long_avg}\n")
                f.flush()
#             else:
#                f.write("NO,")
 
