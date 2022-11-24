# Made by @jradaco (github.com/jradaco, https://juanser.com/)

from typing import List
import re
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd


class ProbeRequest:
    mac: str
    timeStamp: datetime
    rssi: str
    ids: tuple

    def __init__(self, rssi, mac, ids, timeStamp):
        self.rssi = rssi
        self.mac = mac
        self.ids = ids
        self.timeStamp = timeStamp

    def __str__(self) -> str:
        return f"time: {self.timeStamp} rssi: {self.rssi} mac: {self.mac} ies: {self.ids}"


class Device:
    hash = str
    timeStamps = list


def main():
    testProbeRequest = "-57 32:12:CB:7C:64:53 B7 0 0 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 12 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,38 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "
    testProbeRequest1 = "-56 32:12:CB:7C:64:53 B8 0 13 83,73,76,86,69,82,67,79,78,32,32,53,103 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 12 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,38 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "
    testProbeRequest2 = "-54 32:12:CB:7C:64:53 BD 0 0 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 13 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,38 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "
    testProbeRequest3 = "-54 32:12:CB:7C:64:53 BE 0 13 83,73,76,86,69,82,67,79,78,32,32,53,103 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 13 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,38 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "
    testProbeRequest4 = "-54 32:12:CB:7C:64:53 BF 0 0 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 13 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,18 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "

    probeRequestListSerial = [testProbeRequest, testProbeRequest1,
                              testProbeRequest2, testProbeRequest3, testProbeRequest4]

    with open("captura_assorted.txt") as archivo:
        lineas = archivo.readlines()

    probeRequestList = []

    # for prb in probeRequestListSerial:
    for prb in lineas:
        try:
            aux_rssi = re.findall(r"(-\d\d)", prb)

            aux_mac = re.findall(r"((?:[0-9a-fA-F]:?){7,12})", prb)
            prb = re.sub(
                r"((?:[0-9a-fA-F]:?){7,12}\s[0-9a-fA-F]{1,3})", "|", prb)

            aux_ids = re.findall(r"(\d+)\s\d+\s(?:\d+,)+\d+", prb)
            prb = re.sub(r"(\d+\s\d+\s(?:\d+,)+\d+)", "|", prb)

            aux_ids.extend(re.findall(r"\s(\d+)\s[0|1](?:\s\d+)?", prb))
            aux_ids.sort()

            aux_timeStamp = re.findall(r"(\d+:\d+:\d+.\d+)", prb)[0]

            aux = ProbeRequest(
                aux_rssi[0], aux_mac[0], tuple(aux_ids), datetime.strptime(aux_timeStamp, '%H:%M:%S.%f'))
            probeRequestList.append(aux)
        except:
            pass

    print_log("####### Listado de probe requests ########")
    print_log("len " + str(len(probeRequestList)))
    print_log("####### Listado de dispositivos ########")
    a = extract_sets_device(probeRequestList)
    print_log(str(a["deviceSet"]))
    print_log("Numero dispositivos: " + str(len(a["deviceSet"])))
    print_log("####### Identificador y Horas ########")
    print_log(str(a["deviceDictionary"]))
    for (key, value) in a["deviceDictionary"].items():
        print_log(f"# numero de macs para {str(key)}: {str(len(value))} #")
    print_log("####### delta prb_req ########")
    delta_prb = give_me_deltatime_prb_req_per_mac(a["deviceDictionary"])
    print_log(str(delta_prb))
    print_log("####### plot hist delta prb ########")
    delta_prb_df = pd.DataFrame(delta_prb, columns=['Delta ProbeReq'])
    conversion = delta_prb_df/pd.Timedelta(milliseconds=1)
    print_log(str(conversion))
    plt.hist(conversion, bins=20)
    plt.show()
    print_log("####### delta_rafaga dict ########")
    delta_rafaga = give_me_deltatime_rafaga(a["deviceDictionary"])
    print_log(str(delta_rafaga.items()))
    print_log("####### plot hist delta rafaga per device ########")
    df_list = []
    for name, device in delta_rafaga.items():
        aux_delta_rafaga_df = pd.DataFrame(device, columns=[name])
        df_list.append(aux_delta_rafaga_df)

    # hola a todoss
    for df in df_list:
        conversion_rafaga = df/pd.Timedelta(milliseconds=1)
        print_log(f"dataset df")
        plt.hist(conversion_rafaga, bins=20)
        plt.show()

    print_log("############################")


def check_ies_equal_sets(deviceList: list(), iesSet: set()):
    for device in deviceList:
        if device.ies == iesSet:
            return True
        else:
            return False


def extract_sets_device(probeRequestList: list()):
    deviceSet = set()
    macsBuscadas = list()
    deviceDictionary = dict()
    for probeReq in probeRequestList:
        if probeReq.mac not in macsBuscadas:
            macListFiltered = [
                x for x in probeRequestList if x.mac == probeReq.mac]
            auxFrozenSet = put_ies_in_set_per_mac(macListFiltered)
            deviceSet.add(auxFrozenSet)
            auxFrozenHash = calculate_hash(auxFrozenSet)
            if auxFrozenHash not in deviceDictionary:
                deviceDictionary[auxFrozenHash] = []
            deviceDictionary[auxFrozenHash].append(
                put_timestamps_in_list_per_mac(macListFiltered))
            macsBuscadas.append(probeReq.mac)
    return {"deviceSet": deviceSet, "deviceDictionary": deviceDictionary}


def put_ies_in_set_per_mac(probeRequestList: list()):
    iesSet = set()
    for probReq in probeRequestList:
        print(f"prb req per mac {probReq.ids}")
        iesSet.add(probReq.ids)
    print(f"termino per mac {iesSet}")
    return frozenset(iesSet)


def print_log(texto):
    with open('debug.txt', 'a') as f:
        f.write(str(texto) + '\n')


def calculate_hash(iesFrozenSet: frozenset()):
    # return iesFrozenSet.__hash__()
    return str(iesFrozenSet)


def put_timestamps_in_list_per_mac(probeRequestList: list()):
    timeList = list()
    for probReq in probeRequestList:
        timeList.append(probReq.timeStamp)
    return timeList


def give_me_ies_per_prb_req(prb):
    prb = re.sub(r"(-\d\d)", "|", prb)
    prb = re.sub(r"((?:[0-9a-fA-F]:?){7,12}\s[0-9a-fA-F]{1,3})", "|", prb)

    aux_ids = re.findall(r"(\d+)\s\d+\s(?:\d+,)+\d+", prb)
    prb = re.sub(r"(\d+\s\d+\s(?:\d+,)+\d+)", "|", prb)

    aux_ids.extend(re.findall(r"\s(\d+)\s[0|1](?:\s\d+)?", prb))

    print_log(str(aux_ids))
    print_log("#")


def give_me_deltatime_prb_req_per_mac(deviceDictionary: dict()):
    delta_prbreq = []
    for (key, value) in deviceDictionary.items():
        for macList in value:
            for i in range(len(macList)):
                if i < len(macList) - 1:
                    delta_time = macList[i+1] - macList[i]
                    delta_prbreq.append(delta_time)
    return delta_prbreq


def give_me_deltatime_rafaga(deviceDictionary: dict()):
    delta_rafaga = {}
    for (key, value) in deviceDictionary.items():
        for i in range(len(value)):
            if i < len(value) - 1:
                delta_time = value[i+1][0] - value[i][0]
                if key not in delta_rafaga:
                    delta_rafaga[key] = []
                delta_rafaga[key].append(delta_time)
    return delta_rafaga
