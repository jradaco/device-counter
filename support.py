# Made by @jradaco (github.com/jradaco, https://juanser.com/)

from typing import List
import time
import datetime
import re


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


class Device:
    id = ""
    probeRequests = []
    ies = set()


def main():
    testProbeRequest = "-57 32:12:CB:7C:64:53 B7 0 0 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 12 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,38 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "
    testProbeRequest1 = "-56 32:12:CB:7C:64:53 B8 0 13 83,73,76,86,69,82,67,79,78,32,32,53,103 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 12 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,38 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "
    testProbeRequest2 = "-54 32:12:CB:7C:64:53 BD 0 0 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 13 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,38 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "
    testProbeRequest3 = "-54 32:12:CB:7C:64:53 BE 0 13 83,73,76,86,69,82,67,79,78,32,32,53,103 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 13 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,38 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "
    testProbeRequest4 = "-54 32:12:CB:7C:64:53 BF 0 0 1 4 2,4,11,22 50 8 12,18,24,36,48,72,96,108 3 1 13 45 26 173,1,19,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 127 10 4,0,10,2,0,64,0,64,128,1 191 12 146,249,145,51,250,255,12,3,250,255,12,3 221 7 0,80,242,8,0,30,0 255 3 2,0,18 127 10 0,0,10,2,0,64,0,0,0,1 255 3 2,0,255 221 10 80,111,154,22,3,1,3,101,1,1 221 8 140,253,240,1,1,2,1,0 "

    probeRequestListSerial = [testProbeRequest, testProbeRequest1,
                              testProbeRequest2, testProbeRequest3, testProbeRequest4]

    with open("captura_30_10.txt") as archivo:
        lineas = archivo.readlines()

    probeRequestList = []

    # for prb in probeRequestListSerial:
    for prb in lineas:
        try:
            aux_rssi = re.findall(r"(-\d\d)", prb)

            aux_mac = re.findall(r"((?:[0-9a-fA-F]:?){7,12})", prb)
            prb = re.sub(
                r"((?:[0-9a-fA-F]:?){7,12}\s[0-9a-fA-F]{1,3})", "|", prb)

            aux_ids = set(re.findall(r"(\d+)\s\d+\s(?:\d+,)+\d+", prb))
            prb = re.sub(r"(\d+\s\d+\s(?:\d+,)+\d+)", "|", prb)

            aux_ids.update(re.findall(r"\s(\d+)\s[0|1](?:\s\d+)?", prb))

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


def check_ies_equal_sets(deviceList: list(), iesSet: set()):
    for device in deviceList:
        if device.ies == iesSet:
            return True
        else:
            return False


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
    with open('debug.txt', 'a') as f:
        f.write(str(texto) + '\n')
