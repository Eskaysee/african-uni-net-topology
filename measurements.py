from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)

import IP_hostReader

addresses = IP_hostReader.uniData

ATLAS_API_KEY = "ee507b44-4052-4c46-89f6-d8d4b447af4b"

#Probes
namibia = AtlasSource(
    type="country",
    value="NA",
    requested=3
)

senegal = AtlasSource(
    type="country",
    value="SN",
    requested=3
)
malawi = AtlasSource(
    type="country",
    value="MW",
    requested=3
)

rsa = AtlasSource(
    type="probes",
    value="25200,60408,1004024",
    requested=3
)

cameroon = AtlasSource(
    type="probes",
    value="32597,1003759,7050",
    requested=3
)

tanzania = AtlasSource(
    type="probes",
    value="19925,20772,24798",
    requested=3
)

morocco = AtlasSource(
    type="probes",
    value="62159,12344,32925",
    requested=3
)

for domainName in addresses:
    ping = Ping(
        af=4,
        target= str(addresses[domainName]),
        description="Ping measurement Test to " + domainName,
        packets = 5,
        size = 48,
        interval = 28800,
        resolve_on_probe = True,
        skip_dns_check = False,
        include_probe_id = True
    )

    traceroute = Traceroute(
        af=4,
        target= str(addresses[domainName]),
        description="Traceroute measurement Test to " + domainName,
        protocol="ICMP",
        response_timeout = 4000,
        interval = 28800,
        resolve_on_probe = True,
        packets = 7,
        size = 48,
        first_hop = 1,
        max_hops = 32,
        paris = 16,
        destination_option_size = 0,
        hop_by_hop_option_size = 0,
        dont_fragment = False,
        skip_dns_check = False
    )

    atlas_request = AtlasCreateRequest(
        start_time=1694323800,
        stop_time = 1694556000,
        key=ATLAS_API_KEY,
        measurements=[ping, traceroute],
        sources=[namibia, senegal, malawi, rsa, cameroon, tanzania, morocco],
        is_oneoff=False,
        bill_to = "sihlecalana@gmail.com"
    )

    (is_success, response) = atlas_request.create()

    print(f"Measurement test for {domainName}({str(addresses[domainName])})")
    print("success? " + str(is_success))
    print("response: " + str(response))
    print("\n-------------------------------------------------------------------------------------\n")