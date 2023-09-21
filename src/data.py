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
    AsnPaths, CountryPaths = [], []
    for probe in pData[country]:
        for date in pData[country][probe]:
            if pData[country][probe][date][0] != {}: 
                if pData[country][probe][date][0]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][0]["average_RTT"] != -1:
                        mornRTTs.append(pData[country][probe][date][0]["average_RTT"])
                    mornPLs.append(float(pData[country][probe][date][0]["packet_loss"].split("%")[0]))
                    mornAShops.append(tData[country][probe][date][0]["AS_hops"])
                    mornCountHops.append(tData[country][probe][date][0]["countryHops"])
                    AsnPaths.append(tData[country][probe][date][0]["asn_path"])
                    CountryPaths.append(tData[country][probe][date][0]["country_path"])

            if pData[country][probe][date][1] != {}: 
                if pData[country][probe][date][1]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][1]["average_RTT"] != -1:
                        noonRTTs.append(pData[country][probe][date][1]["average_RTT"])
                    noonPLs.append(float(pData[country][probe][date][1]["packet_loss"].split("%")[0]))
                    noonAShops.append(tData[country][probe][date][1]["AS_hops"])
                    noonCountHops.append(tData[country][probe][date][1]["countryHops"])
                    AsnPaths.append(tData[country][probe][date][1]["asn_path"])
                    CountryPaths.append(tData[country][probe][date][1]["country_path"])
            
            if pData[country][probe][date][2] != {}: 
                if pData[country][probe][date][2]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][2]["average_RTT"] != -1:
                        eveRTTs.append(pData[country][probe][date][2]["average_RTT"])
                    evePLs.append(float(pData[country][probe][date][2]["packet_loss"].split("%")[0]))
                    eveAShops.append(tData[country][probe][date][2]["AS_hops"])
                    eveCountHops.append(tData[country][probe][date][2]["countryHops"])
                    AsnPaths.append(tData[country][probe][date][2]["asn_path"])
                    CountryPaths.append(tData[country][probe][date][2]["country_path"])
            
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

    hopRTTData = {"avgMornRtt": mornRTT, "avgNoonRtt": noonRTT, "avgEveRtt": eveRTT, "minASNPath": min(AsnPaths,key=len), 
     "maxASNPath": max(AsnPaths,key=len), "minCountryPath": min(CountryPaths,key=len), "maxCountryPath": max(CountryPaths,key=len)}

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
            details[srcNation].append({uni: [round(i,2) for i in arr[:2]]+[round(hop) for hop in arr[2:]]})
        else:
            findings[destNation].append(arr)
            details[destNation].append({uni: [round(i,2) for i in arr[:2]]+[round(hop) for hop in arr[2:]]})
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

print(analysis1)

def generalInterFrom(country):
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
        periodRTT = [mornRtt, noonRtt, eveRtt]
        periodRTT = [round(mean(rtt),2) for rtt in periodRTT]
        result[country] = periodRTT
    return result

def hopsData():
    for source in country2site:
        f = open(f"{source}/hopsToCountries.csv",'w')
        f.write("destCountry;website;PacketLoss;minASPath;maxASPath;minCountryPath;maxCountryPath\n")
        for dest in country2site[source]:
            for i in range(0, len(country2site[source][dest])):
                for site in country2site[source][dest][i]:
                    f.write(dest+';')
                    f.write(site+';')
                    if source == dest: f.write(str(a1_deets[source][i][site][0])+';')
                    else: f.write(str(a2_deets[source][dest][i][site][0])+';')
                    f.write(str(country2site[source][dest][i][site]["minASNPath"])+';')
                    f.write(str(country2site[source][dest][i][site]["maxASNPath"])+';')
                    f.write(str(country2site[source][dest][i][site]["minCountryPath"])+';')
                    f.write(str(country2site[source][dest][i][site]["maxCountryPath"])+'\n')
        f.close()