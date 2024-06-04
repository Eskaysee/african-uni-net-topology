from ripe.atlas.cousteau import (
    AtlasResultsRequest,
    Probe
)
import json, os, geoip2.database, statistics
from datetime import datetime, time
import concurrent.futures

countries = {"ZA" : "South Africa", "NA" : "Namibia", "TZ" : "Tanzania", "MA": "Morocco", "SN" : "Senegal", "MW" : "Malawi", "CM" : "Cameroon"}

def timeOday(utctime):
    morning = time(5,0,0)
    afternoon = time(13,0,0)
    evening = time(21,0,0)
    Mtime = datetime.utcfromtimestamp(utctime).time()
    if morning <= Mtime <= afternoon:
        return 0#'morning(05:30 GMT)'
    elif afternoon <= Mtime <= evening:
        return 1#'afternoon(13:30 GMT)'
    elif evening <= Mtime:
        return 2#'evening(21:30 GMT)'
    return 'failed'

def deadPackets(sent, received):
    return ((sent - received)/sent)*100

def meanRTT(rtts):
    #check for timed out or dead packets (ttl<=0)
    i = 0
    while i<len(rtts):
        if rtts[i] == "*": del rtts[i]
        else: i += 1
    if rtts == []: return "timeout"
    elif len(rtts) == 1: return rtts[0]
    #remove outliers
    Q1 = statistics.quantiles(rtts, n=4, method="inclusive")[0]
    Q3 = statistics.quantiles(rtts, n=4, method="inclusive")[2]
    IQR = Q3 - Q1
    lowerFence = Q1 - (1.5 * IQR)
    upperFence = Q3 + (1.5 * IQR)
    for rtt in rtts:
        if rtt < lowerFence or rtt > upperFence:
            rtts.remove(rtt)
    #return the average
    return statistics.mean(rtts)

countryReader = geoip2.database.Reader('GeoLite2-Country.mmdb')
asnReader = geoip2.database.Reader('GeoLite2-ASN.mmdb')

def traces(res2):
    traceData = {}
    measrNo = 0
    target = res2[0]["dst_addr"]
    for data in res2:
        if data["msm_name"] != "Traceroute": break
        probe = Probe(id=data["prb_id"])
        country = countries[probe.country_code]
        isConnected = False
        asnPath = [probe.asn_v4]
        countryPath = [country]
        IPs = []
        for hop in data["result"]:
            countryData, asnData, ip = "", "", ""
            packet_rtts = []
            try:
                for packet in hop["result"]:
                    try:
                        if countryData == "" and asnData == "":
                            countryData = countryReader.country(packet["from"])
                            asnData = asnReader.asn(packet["from"])
                            ip = packet["from"]
                            if packet["from"] == target: isConnected = True
                        packet_rtts.append(packet["rtt"])
                    except KeyError:
                        if countryData == "" or asnData == "":
                            asnData = "N/A"
                            countryData = "N/A"
                        break
                    except geoip2.errors.AddressNotFoundError:
                        if countryData == "" or asnData == "":
                            temp = os.popen(f"geoiplookup {packet['from']}").read().strip().split(", ")
                            if len(temp) == 1:
                                countryData = "N/A"
                                asnData = "N/A"
                            else: 
                                ip = packet["from"]
                                countryData = temp[1]
                                asnData = "None"
                        if asnData == "None":
                            packet_rtts.append(packet["rtt"])
            except KeyError:
                break
            if (
                countryData != "N/A" and asnData != "N/A"
                and asnData != "None"
            ): 
                if (
                    countryData.country.name != countryPath[-1] or 
                    asnData.autonomous_system_number != asnPath[-1] 
                ):
                    IPs.append({"ip": ip,"asn":asnData.autonomous_system_number,"country":countryData.country.name.strip(),"rtt":meanRTT(packet_rtts)})
                if asnData.autonomous_system_number != asnPath[-1]: asnPath.append(asnData.autonomous_system_number)
                if countryData.country.name != countryPath[-1]: countryPath.append((countryData.country.name.strip()))
            elif countryData == "N/A" and asnData == "N/A": continue
            else:
                if countryData != countryPath[-1] and type(countryData)==type(""): 
                    countryPath.append(countryData)
                    IPs.append({"ip": ip, "asn": "None", "country":countryData,"rtt":meanRTT(packet_rtts)})
        date = str(datetime.fromtimestamp(data["timestamp"]).date())
        mTime = timeOday(data["timestamp"])
        info = {"AS_hops":len(asnPath)-1, "countryHops":len(countryPath)-1, "asn_path": asnPath, "country_path": countryPath, "Connected": isConnected, "IPs:": IPs}
        try:
            traceData[country][probe.id][date][mTime] = info
        except KeyError:
            try:
                traceData[country][probe.id][date] = [{}]*3
                traceData[country][probe.id][date][mTime] = info
            except KeyError:
                try:
                    traceData[country][probe.id] = {}
                    traceData[country][probe.id][date] = [{}]*3
                    traceData[country][probe.id][date][mTime] = info
                except KeyError:
                    traceData[country] = {}
                    traceData[country][probe.id] = {}
                    traceData[country][probe.id][date] = [{}]*3
                    traceData[country][probe.id][date][mTime] = info
        measrNo += 1
        print("tm:", measrNo)
    return traceData

def pings(res1):
    pingData = {}
    measrNo = 0
    for data in res1:
        if data["msm_name"] != "Ping": break
        probe = Probe(id=data["prb_id"])
        probeCountry = countries[probe.country_code]
        avgRTT = data["avg"]
        date = str(datetime.fromtimestamp(data["timestamp"]).date())
        mTime = timeOday(data["timestamp"])
        minRTT, maxRTT = data["min"], data["max"]
        try:
            packetLoss = f"{deadPackets(data['sent'], data['rcvd'])}%"
            num = min(abs(avgRTT-minRTT),abs(maxRTT-avgRTT))
            if (maxRTT > (avgRTT + 2*num) 
                or minRTT < (avgRTT - 2*num)):
                RTTs = []
                for packet in data["result"]:
                    RTTs.append(packet["rtt"])
                avgRTT = meanRTT(RTTs)
        except ZeroDivisionError:
            packetLoss = "No Packets Sent"
        except KeyError:
            packetLoss = f"{deadPackets(data['sent'], data['rcvd'])}%"
        info = {"packet_loss": packetLoss, "average_RTT": avgRTT, "min_RTT": minRTT, "max_RTT": maxRTT}
        try:
            pingData[probeCountry][probe.id][date][mTime] = info
        except KeyError:
            try:
                pingData[probeCountry][probe.id][date] = [{}]*3
                pingData[probeCountry][probe.id][date][mTime] = info
            except KeyError:
                try:
                    pingData[probeCountry][probe.id] = {}
                    pingData[probeCountry][probe.id][date] = [{}]*3
                    pingData[probeCountry][probe.id][date][mTime] = info
                except KeyError:
                    pingData[probeCountry] = {}
                    pingData[probeCountry][probe.id] = {}
                    pingData[probeCountry][probe.id][date] = [{}]*3
                    pingData[probeCountry][probe.id][date][mTime] = info
        measrNo += 1
        print("pm:", measrNo)
    return pingData

f = open("measurements.txt", "r")
measurements = eval(str(f.read()))
f.close()
progress = 0
for uni in measurements:
    path = countries[(uni[-2:]).upper()]
    print('\n', "uni:", uni, '\n')
    #os.mkdir(path)
    #os.mkdir(f"{path}/{uni}")
    kwargs = {
        "msm_id": measurements[uni][0]
    }
    is_success1, results = AtlasResultsRequest(**kwargs).create()
    res1 = json.loads(str(results).replace("'", "\""))

    kwargs = {
        "msm_id": measurements[uni][1]
    }
    is_success2, results = AtlasResultsRequest(**kwargs).create()
    res2 = json.loads(str(results).replace("'", "\""))

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    
    thread1 = executor.submit(pings, res1)
    thread2 = executor.submit(traces, res2)

    pingData, traceData = thread1.result(), thread2.result()

    executor.shutdown()

    pingf = open(f"{path}/{uni}/Ping.json", "w")
    if is_success1:
        json.dump(pingData, pingf, indent=4)
    pingf.close()
    
    tracef = open(f"{path}/{uni}/Traceroute.json", "w")
    if is_success2:
        json.dump(traceData, tracef, indent=4)
    tracef.close()

    progress+=1
    percent = progress/len(measurements)*100
    print(f"{progress}/{len(measurements)} ({percent}%) university measurements completed")

countryReader.close()
asnReader.close()
