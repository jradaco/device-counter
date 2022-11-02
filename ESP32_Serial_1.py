# Made by @xdavidhu (github.com/xdavidhu, https://xdavidhu.me/)

import serial
import re
import io
import os
import subprocess
import signal
import time
import datetime


class ProbeRequest:
    mac: str
    timeStamp: float
    rssi: str
    ids: frozenset

    def __init__(self, rssi, mac, ids, timeStamp):
        self.rssi = rssi
        self.mac = mac
        self.ids = ids
        self.timeStamp = timeStamp

    def __str__(self) -> str:
        return f"time: {self.timeStamp} rssi: {self.rssi} mac: {self.mac} ies: {self.ids}"


def main():

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
    timeout = 60  # [seconds]
    timeout_start = time.time()
    index = 0
    try:
        while True:
            serialLines = []
            while time.time() < timeout_start + timeout:
                ch = ser.readline()
                serialLines.append(str(ch))
            time.sleep(1)
            print_log(f"## PRB Requests Capturados # {index}:")
            print_log(serialLines)
            print_log(f"####")

            probeRequestList = []
            for prb in serialLines:
                try:
                    aux_rssi = re.findall(r"(-\d\d)", prb)

                    aux_mac = re.findall(r"((?:[0-9a-fA-F]:?){7,12})", prb)
                    prb = re.sub(
                        r"((?:[0-9a-fA-F]:?){7,12}\s[0-9a-fA-F]{1,3})", "|", prb)

                    aux_ids = set(re.findall(r"(\d+)\s\d+\s(?:\d+,)+\d+", prb))
                    prb = re.sub(r"(\d+\s\d+\s(?:\d+,)+\d+)", "|", prb)

                    aux_ids.update(re.findall(
                        r"\s(\d+)\s[0|1](?:\s\d+)?", prb))

                    aux_timeStamp = time.time()
                    aux = ProbeRequest(
                        aux_rssi[0], aux_mac[0], frozenset(aux_ids), aux_timeStamp)
                    probeRequestList.append(aux)
                except:
                    pass

            print_log("####### Listado de probe requests ########")
            print_log("len " + str(len(probeRequestList)))
            print_log("####### Listado de dispositivos ########")
            a = extract_sets_device(probeRequestList)
            num_devices = 0
            for device in a:
                print_log("--------")
                print_log(device)
                if len(device) == 1:
                    num_devices = num_devices + 1
                print_log("--------")
            print_log("Numero dispositivos: " + str(num_devices))
            print_log("############################")

    except KeyboardInterrupt:
        print("[+] Stopping...")

    ser.close()
    print("[+] Done.")


def extract_sets_device(probeRequestList: list()):
    deviceSet = set()
    macsBuscadas = set()
    for probeReq in probeRequestList:
        if probeReq.mac not in macsBuscadas:
            macListFiltered = [
                x for x in probeRequestList if x.mac == probeReq.mac]
            deviceSet.add(put_ies_in_set_per_mac(macListFiltered))
            macsBuscadas.add(probeReq.mac)
    return deviceSet


def put_ies_in_set_per_mac(probeRequestList: list()):
    iesSet = set()
    for probReq in probeRequestList:
        iesSet.add(probReq.ids)
    return frozenset(iesSet)


def print_log(texto):
    with open('debug.log', 'a') as f:
        f.write(str(texto) + '\n')
