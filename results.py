from ripe.atlas.cousteau import AtlasResultsRequest
import json, os

f = open("measurements.txt", "r")
measurements = eval(str(f.read()))
f.close()
os.mkdir("results")

for uni in measurements:
    os.mkdir(f"results/{uni}")
    pingf = open(f"results/{uni}/Ping.json", "w")
    kwargs = {
        "msm_id": measurements[uni][0]
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()
    res1 = json.loads(str(results).replace("'", "\""))
    if is_success:
        json.dump(res1, pingf, indent=4)
    pingf.close()

    tracef = open(f"results/{uni}/Traceroute.json", "w")
    kwargs = {
        "msm_id": measurements[uni][1]
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()
    res2 = json.loads(str(results).replace("'", "\""))
    if is_success:
        json.dump(res2, tracef, indent=4)
    tracef.close()