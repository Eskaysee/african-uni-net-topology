import statistics, os

def mean(arr):
    if arr == []: return -1
    return statistics.mean(arr)

country2site = {}

def country2target(country, pData, tData):
    mornPLs, noonPLs, evePLs = [], [], []
    mornRTTs, noonRTTs, eveRTTs = [], [], []
    mornAShops, noonAShops, eveAShops = [], [], []
    mornCountHops, noonCountHops, eveCountHops = [], [], []
    minASNPath, maxASNPath, minCountryPath, maxCountryPath = [], [], [], []
    for probe in pData[country]:
        for date in pData[country][probe]:
            if pData[country][probe][date][0] != {}: 
                if pData[country][probe][date][0]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][0]["average_RTT"] != -1:
                        mornRTTs.append(pData[country][probe][date][0]["average_RTT"])
                    mornPLs.append(float(pData[country][probe][date][0]["packet_loss"].split("%")[0]))
                    mornAShops.append(tData[country][probe][date][0]["AS_hops"])
                    mornCountHops.append(tData[country][probe][date][0]["countryHops"])
                    if (minASNPath == [] and  maxCountryPath == []):
                        minASNPath = tData[country][probe][date][0]["asn_path"]
                        maxASNPath = tData[country][probe][date][0]["asn_path"]
                        minCountryPath = tData[country][probe][date][0]["country_path"]
                        maxCountryPath = tData[country][probe][date][0]["country_path"] 
                    elif mornAShops[-1] < len(minASNPath)-1:
                        minASNPath = tData[country][probe][date][0]["asn_path"]
                    elif mornAShops[-1] > len(maxASNPath)-1:
                        maxASNPath = tData[country][probe][date][0]["asn_path"]
                    if mornCountHops[-1] < len(minCountryPath)-1:
                        minCountryPath = tData[country][probe][date][0]["country_path"]
                    elif mornCountHops[-1] > len(maxCountryPath)-1:
                        maxCountryPath = tData[country][probe][date][0]["country_path"]

            if pData[country][probe][date][1] != {}: 
                if pData[country][probe][date][1]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][1]["average_RTT"] != -1:
                        noonRTTs.append(pData[country][probe][date][1]["average_RTT"])
                    noonPLs.append(float(pData[country][probe][date][1]["packet_loss"].split("%")[0]))
                    noonAShops.append(tData[country][probe][date][1]["AS_hops"])
                    noonCountHops.append(tData[country][probe][date][1]["countryHops"])
                    if (minASNPath == [] and  maxCountryPath == []):
                        minASNPath = tData[country][probe][date][1]["asn_path"]
                        maxASNPath = tData[country][probe][date][1]["asn_path"]
                        minCountryPath = tData[country][probe][date][1]["country_path"]
                        maxCountryPath = tData[country][probe][date][1]["country_path"]
                    elif noonAShops[-1] < len(minASNPath)-1:
                        minASNPath = tData[country][probe][date][1]["asn_path"]
                    elif noonAShops[-1] > len(maxASNPath)-1:
                        maxASNPath = tData[country][probe][date][1]["asn_path"]
                    if noonCountHops[-1] < len(minCountryPath)-1:
                        minCountryPath = tData[country][probe][date][1]["country_path"]
                    elif noonCountHops[-1] > len(maxCountryPath)-1:
                        maxCountryPath = tData[country][probe][date][1]["country_path"]
            
            if pData[country][probe][date][2] != {}: 
                if pData[country][probe][date][2]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][2]["average_RTT"] != -1:
                        eveRTTs.append(pData[country][probe][date][2]["average_RTT"])
                    evePLs.append(float(pData[country][probe][date][2]["packet_loss"].split("%")[0]))
                    eveAShops.append(tData[country][probe][date][2]["AS_hops"])
                    eveCountHops.append(tData[country][probe][date][2]["countryHops"])
                    if (minASNPath == [] and  maxCountryPath == []):
                        minASNPath = tData[country][probe][date][2]["asn_path"]
                        maxASNPath = tData[country][probe][date][2]["asn_path"]
                        minCountryPath = tData[country][probe][date][2]["country_path"]
                        maxCountryPath = tData[country][probe][date][2]["country_path"]
                    elif eveAShops[-1] < len(minASNPath)-1:
                        minASNPath = tData[country][probe][date][2]["asn_path"]
                    elif eveAShops[-1] > len(maxASNPath)-1:
                        maxASNPath = tData[country][probe][date][2]["asn_path"]
                    if eveCountHops[-1] < len(minCountryPath)-1:
                        minCountryPath = tData[country][probe][date][2]["country_path"]
                    elif eveCountHops[-1] > len(maxCountryPath)-1:
                        maxCountryPath = tData[country][probe][date][2]["country_path"]
    mornPL = mean(mornPLs)
    noonPL = mean(noonPLs)
    evePL = mean(evePLs)
    mornRTT = mean(mornRTTs)
    noonRTT = mean(noonRTTs) 
    eveRTT = mean(eveRTTs)
    mornAShop = mean(mornAShops)
    noonAShop = mean(noonAShops)
    eveAShop = mean(eveAShops)
    mornCountHop = mean(mornCountHops)
    noonCountHop = mean(noonCountHops)
    eveCountHop = mean(eveCountHops)

    hopRTTData = {"avgMornRtt": mornRTT, "avgNoonRtt": noonRTT, "avgEveRtt": eveRTT, "minASNPath": minASNPath, 
     "maxASNPath": maxASNPath, "minCountryPath": minCountryPath, "maxCountryPath": maxCountryPath}

    pl = mean([mornPL, noonPL, evePL])
    rtt = mean([mornRTT, noonRTT, eveRTT])
    asnHops = mean([mornAShop, noonAShop, eveAShop])
    country_hops = mean([mornCountHop, noonCountHop, eveCountHop])
    return [pl, rtt, asnHops, country_hops], hopRTTData

def consolidate(lib, country):
    pl, rtt, asnHops, country_hops = [], [], [], []
    for i in range(0, len(lib[country])):
        pl.append(lib[country][i][0])
        if lib[country][i][1] != -1:
            rtt.append(lib[country][i][1])
        asnHops.append(lib[country][i][2])
        country_hops.append(lib[country][i][3])
    return [round(mean(pl),2), round(mean(rtt),2), round(mean(asnHops)), round(mean(country_hops))]

def results(srcNation, destNation, findings, details):
    unis = os.listdir(f"{destNation}")
    for uni in unis:
        if uni[-3:] in ["png","csv","txt"]: continue
        pfile = open(f"{destNation}/{uni}/Ping.json", "r")
        tfile = open(f"{destNation}/{uni}/Traceroute.json", "r")
        pingData = eval(str(pfile.read()))
        temp = str(tfile.read()).replace("true", "True")
        traceData = eval(temp.replace("false", "False"))
        pfile.close(), tfile.close()
        arr, hopRttData = country2target(srcNation, pingData, traceData)
        country2site[srcNation][destNation].append({uni:hopRttData})
        if srcNation == destNation:
            findings[srcNation].append(arr)
            details[srcNation].append({uni: [round(i,2) for i in arr]})
        else:
            findings[destNation].append(arr)
            details[destNation].append({uni: [round(i,2) for i in arr]})
    if srcNation == destNation:
        findings[srcNation] = consolidate(findings, srcNation)
    else: findings[destNation] = consolidate(findings, destNation)


countries = {"South Africa", "Namibia", "Malawi", "Tanzania", "Morocco", "Senegal", "Cameroon"}

analysis1 = {}
a1_deets = {}
analysis2 = {}
a2_deets = {}
for country in countries:
    country2site[country] = {}
    country2site[country][country] = []
    analysis1[country] = []
    a1_deets[country] = []
    analysis2[country] = {}
    a2_deets[country] = {}
    results(country, country, analysis1, a1_deets)
    elsewhere = [nation for nation in countries if nation not in country]
    for nation in elsewhere:
        country2site[country][nation] = []
        analysis2[country][nation] = []
        a2_deets[country][nation] = []
        results(country, nation, analysis2[country], a2_deets[country])

def generalIntra():
    return analysis1, a1_deets

def generalInter():
    return analysis2, a2_deets

def generalInter(country):
    return analysis2[country], a2_deets[country]

def periodRttData(nation):
    result = {}
    for country in country2site[nation]:
        periodRTT = []
        mornRtt, noonRtt, eveRtt = [], [], []
        for i in range(0, len(country2site[nation][country])):
            for uni in country2site[nation][country][i]:
                if country2site[nation][country][i][uni]["avgMornRtt"] != -1:
                    mornRtt.append(country2site[nation][country][i][uni]["avgMornRtt"])
                if country2site[nation][country][i][uni]["avgNoonRtt"] != -1:
                    noonRtt.append(country2site[nation][country][i][uni]["avgNoonRtt"])
                if country2site[nation][country][i][uni]["avgEveRtt"] != -1:
                    eveRtt.append(country2site[nation][country][i][uni]["avgEveRtt"])
        periodRTT = [round(mean(mornRtt),2), round(mean(noonRtt),2), round(mean(eveRtt),2)]
        result[country] = periodRTT
    return result

def hopsData():
    for source in country2site:
        for dest in country2site[source]:
            f = open(f"{source}/hopsTo{dest}.csv",'w')
            f.write("minASPath;maxASPath;minCountryPath;maxCountryPath\n")
            for i in range(0, len(country2site[source][dest])):
                for site in country2site[source][dest][i]:
                    f.write(str(country2site[source][dest][i][site]["minASNPath"])+';')
                    f.write(str(country2site[source][dest][i][site]["minASNPath"])+';')
                    f.write(str(country2site[source][dest][i][site]["maxCountryPath"])+';')
                    f.write(str(country2site[source][dest][i][site]["maxCountryPath"])+'\n')
            f.close()