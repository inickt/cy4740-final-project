from collections import defaultdict
import json
import sys
from pprint import pprint

from pyvis.network import Network


def main(data):
    network = Network(height="100%", width="70%")

    flattened_domains = defaultdict(lambda: 1)
    for requests in data.values():
        for request in requests:
            flattened_domains[request["host"]] += 1
    
    pprint(flattened_domains)

    for domain, count in flattened_domains.items():
        network.add_node(domain, label=domain, shape="dot", value=count)

    for label, requests in data.items():
        network.add_node(label, label=label, shape="circle", group=label)
        domains = defaultdict(lambda: 1)
        for request in requests:
            domains[request["host"]] += 1
        for domain, count in domains.items():
            network.add_edge(label, domain, title=str(count), value=count)

    network.force_atlas_2based(
        gravity=-155,
        central_gravity=0.035,
        spring_length=70,
        spring_strength=0.215,
        damping=0.55,
        overlap=1
    )
    network.show_buttons(["physics"])
    network.toggle_physics(True)
    network.show("network.html")


if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        data = json.load(file)
    main(data)
