import graphlib, graphviz, matplotlib, datetime

# def avgRTT(rtts):
#     #check for timed out or dead packets (ttl<=0)
#     i = 0
#     while i<len(rtts):
#         if rtts[i] == "*": del rtts[i]
#         else: i += 1
#     if rtts == []: return "timeout"
#     elif len(rtts) == 1: return rtts[0]
#     #remove outliers
#     try:
#         Q1 = statistics.quantiles(rtts,n=4)[0]
#     except TypeError:
#         print(rtts)
#     Q3 = statistics.quantiles(rtts,n=4)[2]
#     IQR = Q3 - Q1
#     lowerFence = Q1 - (1.5 * IQR)
#     upperFence = Q3 + (1.5 * IQR)
#     for rtt in rtts:
#         if rtt < lowerFence or rtt > upperFence:
#             rtts.remove(rtt)
#     #return the average
#     return statistics.mean(packetRTTs)
