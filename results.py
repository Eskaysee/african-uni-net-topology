from ripe.atlas.cousteau import (
    AtlasResultsRequest,
    Probe
)
import json, os, geoip2.database, statistics
from datetime import datetime, time

countries = {"ZA" : "South Africa", "NA" : "Namibia", "TZ" : "Tanzania", "MA": "Morocco", "SN" : "Senegal", "MW" : "Malawi", "CM" : "Cameroon"}

def timeOday(utctime):
    morning = time(5,0,0)
    afternoon = time(13,0,0)
    evening = time(23,0,0)
    Mtime = datetime.fromtimestamp(utctime).time()
    if morning <= Mtime <= afternoon:
        return 0#'morning(05:30 GMT)'
    elif afternoon <= Mtime <= evening:
        return 1#'afternoon(13:30 GMT)'
    elif evening <= Mtime:
        return 2#'evening(21:30 GMT)'
    return 'failed'

def deadPackets(sent, received):
    return ((sent - received)/sent)*100

countryReader = geoip2.database.Reader('GeoLite2-Country.mmdb')
asnReader = geoip2.database.Reader('GeoLite2-ASN.mmdb')

def traces(res2):
    traceData = {}
    measrNo = 0
    for data in res2:
        if data["msm_name"] != "Traceroute": break
        probe = Probe(id=data["prb_id"])
        country = countries[probe.country_code]
        asnPath = [probe.asn_v4]
        countryPath = [country]
        for hop in data["result"]:
            countryData, asnData = "", ""
            try:
                for packet in hop["result"]:
                    try:
                        if (
                            countryData == "" or asnData == "" 
                            or asnData == "N/A" or countryData == "N/A"
                        ):
                            countryData = countryReader.country(packet["from"])
                            asnData = asnReader.asn(packet["from"])
                    except KeyError:
                        if countryData == "" or asnData == "":
                            asnData = "N/A"
                            countryData = "N/A"
                        continue
                    except geoip2.errors.AddressNotFoundError:
                        if countryData == "" or asnData == "":
                            temp = os.popen(f"geoiplookup {packet['from']}").read().strip().split(", ")
                            if len(temp) == 1:
                                countryData = "N/A"
                            else: countryData = temp[1]
                            asnData = "N/A"
                        continue
            except KeyError:
                break
            if (
                countryData != "N/A" and asnData != "N/A"
                and countryData != "" and asnData != ""
            ): 
                if asnData.autonomous_system_number != asnPath[-1]: asnPath.append(asnData.autonomous_system_number)
                if countryData.country.name != countryPath[-1]: countryPath.append((countryData.country.name.strip()))
            elif countryData == "N/A" and asnData == "N/A":
                if asnData != asnPath[-1]: asnPath.append(asnData)
                if countryData != countryPath[-1] and type(countryData)==type(""): countryPath.append(countryData)
        date = str(datetime.fromtimestamp(data["timestamp"]).date())
        mTime = timeOday(data["timestamp"])
        info = {"AS_hops":len(asnPath), "countryHops":len(countryPath), "asn_path": asnPath, "country_path": countryPath}
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
        try:
            packetLoss = f"{deadPackets(data['sent'], data['rcvd'])}%"
        except ZeroDivisionError:
            packetLoss = "No Packets Sent"
        info = {"packet_loss": packetLoss, "average_RTT": avgRTT, "min_RTT": data["min"], "max_RTT": data["max"]}
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
os.mkdir("results")

for uni in measurements:
    print('\n', "uni:", uni, '\n')
    os.mkdir(f"results/{uni}")
    kwargs = {
        "msm_id": measurements[uni][0]
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()
    res1 = json.loads(str(results).replace("'", "\""))

    kwargs = {
        "msm_id": measurements[uni][1]
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()
    res2 = json.loads(str(results).replace("'", "\""))

    pingData, traceData = pings(res1), traces(res2)

    pingf = open(f"results/{uni}/Ping.json", "w")
    if is_success:
        json.dump(pingData, pingf, indent=4)
    pingf.close()
    
    tracef = open(f"results/{uni}/Traceroute.json", "w")
    if is_success:
        json.dump(traceData, tracef, indent=4)
    tracef.close()

countryReader.close()
asnReader.close()
