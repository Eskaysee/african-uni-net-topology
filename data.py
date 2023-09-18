import statistics, os

def mean(arr):
    if arr == []: return -1
    return statistics.mean(arr)

def intraData(country, pData, tData):
    mornPLs, noonPLs, evePLs = [], [], []
    mornRTTs, noonRTTs, eveRTTs = [], [], []
    mornAShops, noonAShops, eveAShops = [], [], []
    mornCountHops, noonCountHops, eveCountHops = [], [], []
    for probe in pData[country]:
        for date in pData[country][probe]:
            if pData[country][probe][date][0] != {}: 
                if pData[country][probe][date][0]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][0]["average_RTT"] != -1:
                        mornRTTs.append(pData[country][probe][date][0]["average_RTT"])
                    mornPLs.append(float(pData[country][probe][date][0]["packet_loss"].split("%")[0]))
                    mornAShops.append(tData[country][probe][date][0]["AS_hops"])
                    mornCountHops.append(tData[country][probe][date][0]["countryHops"])

            if pData[country][probe][date][1] != {}: 
                if pData[country][probe][date][1]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][1]["average_RTT"] != -1:
                        noonRTTs.append(pData[country][probe][date][1]["average_RTT"])
                    noonPLs.append(float(pData[country][probe][date][1]["packet_loss"].split("%")[0]))
                    noonAShops.append(tData[country][probe][date][1]["AS_hops"])
                    noonCountHops.append(tData[country][probe][date][1]["countryHops"])
            
            if pData[country][probe][date][2] != {}: 
                if pData[country][probe][date][2]["packet_loss"] != "No Packets Sent":
                    if pData[country][probe][date][2]["average_RTT"] != -1:
                        eveRTTs.append(pData[country][probe][date][2]["average_RTT"])
                    evePLs.append(float(pData[country][probe][date][2]["packet_loss"].split("%")[0]))
                    eveAShops.append(tData[country][probe][date][2]["AS_hops"])
                    eveCountHops.append(tData[country][probe][date][2]["countryHops"])
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

    pl = mean([mornPL, noonPL, evePL])
    rtt = mean([mornRTT, noonRTT, eveRTT])
    asnHops = mean([mornAShop, noonAShop, eveAShop])
    country_hops = mean([mornCountHop, noonCountHop, eveCountHop])
    return [pl, rtt, asnHops, country_hops]

def consolidate(lib):
    pl, rtt, asnHops, country_hops = [], [], [], []
    for i in range(0, len(lib[country])):
        pl.append(lib[country][i][0])
        if lib[country][i][1] != -1:
            rtt.append(lib[country][i][1])
        asnHops.append(lib[country][i][2])
        country_hops.append(lib[country][i][3])
    return [round(mean(pl),2), round(mean(rtt),2), round(mean(asnHops)), round(mean(country_hops))]


countries = {"ZA" : "South Africa", "NA" : "Namibia", "TZ" : "Tanzania", "MA": "Morocco", "SN" : "Senegal", "MW" : "Malawi", "CM" : "Cameroon"}
sadc = ["South Africa", "Namibia","Malawi"]
east, north, west, central = ("Tanzania", "Morocco", "Senegal", "Cameroon")
regions = [sadc, east, north, west, central]

ovrl_analysis1 = {}
uni_analysis1 = {}
for country in list(countries.values()):
    ovrl_analysis1[country] = []
    uni_analysis1[country] = []
    unis = os.listdir(f"{country}")
    for uni in unis:
        pfile = open(f"{country}/{uni}/Ping.json", "r")
        tfile = open(f"{country}/{uni}/Traceroute.json", "r")
        pingData = eval(str(pfile.read()))
        temp = str(tfile.read()).replace("true", "True")
        traceData = eval(temp.replace("false", "False"))
        pfile.close(), tfile.close()
        if countries[(uni[-2:]).upper()] == country:
            arr = intraData(country, pingData, traceData)
            ovrl_analysis1[country].append(arr)
            uni_analysis1[country].append({uni: [round(i,2) for i in arr]})
    ovrl_analysis1[country] = consolidate(ovrl_analysis1)

print(ovrl_analysis1)
print(uni_analysis1)