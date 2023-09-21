import matplotlib.pyplot as plt
import numpy as np
import data, os

countries = {"South Africa": "ZA", "Namibia": "NA", "Malawi": "MW", "Tanzania": "TZ", "Morocco": "MA", "Senegal": "SN", "Cameroon": "CM"}

colours = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'white']

def pie(source):
    stats = data.generalInterFrom(source)[0]
    labels = list(stats.keys())
    totNationHops = 0
    hops = []
    for target in labels:
        totNationHops += stats[target][-1]
        hops.append(stats[target][-1])
    explode = [0, 0, 0, 0, 0, 0]
    explode[hops.index(max(hops))] = 0.1
    plt.pie(hops, labels=labels, colors=colours, autopct=lambda p:f'{int(p/100*sum(hops))}({p: .1f}%)', explode=explode, shadow=True)
    plt.title(f'International country hops from {source}')
    plt.savefig(f'{source}/interCountryLevelHops.png', bbox_inches='tight')
    plt.clf()

def bar():
    info = data.generalIntra()[0]
    nations = list(info.keys())
    packetLoss = [info[country][0] for country in nations]
    nations = [countries[i] for i in nations]
    plt.bar(nations, packetLoss, color=colours)
    plt.xlabel("Countries"), plt.ylabel("Ovrl Packet Loss%")
    plt.title("Intranational Packets Lost per Country")
    plt.savefig("intranPacketLoss.png", bbox_inches='tight')
    plt.clf()

def line(country):
    marks = ['o', 's', '+', 'x', 'D', '*']
    styles = ['-', '--', '-.', ':']
    i = 0
    
    period = ["Morn(05.30)", "Noon(13:30)", "Eve(21:30)"]
    periodRTT = data.periodRttData(country)
    for nation in [i for i in periodRTT if periodRTT[i] != ([-1]*3)]:
        plt.plot(period, periodRTT[nation], label=nation, color=colours[i%8], marker=marks[i%6], linestyle=styles[i%4], linewidth=1.5)
        i += 1

    plt.xlabel("Time of Day"), plt.ylabel("Average RTT(ms)")
    plt.title("Average Latency per Period per Country")
    plt.legend()
    plt.savefig(f'{country}/AverageLatencies.png', bbox_inches='tight')
    plt.clf()

data.hopsData()
bar()
for nation in countries:
    line(nation)
    pie(nation)
print("Graphs Generated!")
