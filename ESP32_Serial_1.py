# Made by @xdavidhu (github.com/xdavidhu, https://xdavidhu.me/)

import serial
import io
import os
import subprocess
import signal
import time
import datetime


serialport = "/dev/ttyUSB0"
filename = "Archivos MAC/1_capture.txt"
boardRate = 115200
        
canBreak = False
while not canBreak:
    try:
        ser = serial.Serial(serialport, boardRate)
        canBreak = True
    except KeyboardInterrupt:
        print("\n[+] Exiting...")
        exit()
    except:
        print("[!] Serial connection failed... Retrying...")
        time.sleep(2)
        continue

print("[+] Serial connected. Name: " + ser.name)
counter = 0

start = time.time()
end = time.time()

try:
    while True:
        filename=filename+ str(datetime.datetime.now())+ str(".csv")
        f = open(filename,'wb')
        while (end-start) < 300:
            ch = ser.readline()
            f.write((str(datetime.datetime.now().time())+" ").encode())
            f.write(ch)
            f.flush()
            end = time.time()
        start = time.time()  
        f.close()
        filename = "Archivos MAC/1_capture.txt"
except KeyboardInterrupt:
    print("[+] Stopping...")
        
ser.close()
print("[+] Done.")
