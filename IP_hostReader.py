import geoip2.database
import os

countryReader = geoip2.database.Reader('GeoLite2-Country.mmdb')
asnReader = geoip2.database.Reader('GeoLite2-ASN.mmdb')

university_sites = ["uct.ac.za", "wits.ac.za", "www.sun.ac.za", "cu.edu.eg", "uonbi.ac.ke",
                     "unilag.edu.ng", "ub.bw", "uy1.uninet.cm", "uem.mz", "unam.edu.na",
                       "www.uz.ac.zw", "www.ucad.sn", "www.uneswa.ac.sz", "unima.mw", "udsm.ac.tz",
                         "unza.zm", "ug.edu.gh", "univh2c.ma", "univ-tlemcen.dz", "umc.edu.dz"]

uniData = {}

#terminal
os.system("mkdir uniData")
for site in university_sites:
    os.system("nslookup " + site + " >> uniData/" + site + ".txt")

#get IPs
for site in university_sites:
    file_path = "uniData/" + site + ".txt"
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            ipAddress = lines[-2][9:].strip()
            if ipAddress.find(":") != -1:   #check if its IPv6
                ipAddress = lines[-4][9:].strip()
            uniData[site] = ipAddress
            file.close()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
os.system("rm -r uniData")

os.system("echo \"site,IP,country,asn\" > uniData.csv");
file = open("uniData.csv", "a")
for uni in uniData:
    countryData = countryReader.country(uniData[uni])
    asnData = asnReader.asn(uniData[uni])
    file.write(uni + "," + uniData[uni] + "," + countryData.country.name + "," + str(asnData.autonomous_system_number) + "\n")
    print(uni + " has IP address " + uniData[uni] + " and the server is hosted in " + countryData.country.name + " with ASN " + str(asnData.autonomous_system_number))#organization))

countryReader.close()
asnReader.close()