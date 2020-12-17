from collections import defaultdict
import json
import sys
import os
from pprint import pprint

from pyvis.network import Network


def main(data, name):
    # Set up network
    network = Network(height="100%", width="100%", heading=name)

    # Count total number of visits
    flattened_domains = defaultdict(int)
    for requests in data.values():
        for request in requests:
            flattened_domains[request["host"]] += 1

    # Add node for each domain
    for domain, count in flattened_domains.items():
        labels = defaultdict(int)
        for label, requests in data.items():
            for request in requests:
                if request["host"] == domain:
                    labels[label] += 1

        hover_text = "<b>Sites:</b>"
        for label, count in sorted(labels.items(), key=lambda kv: kv[1], reverse=True):
            hover_text += f"<br>{label} - {count}"
        network.add_node(
            domain, label=domain, shape="dot", value=count, title=hover_text
        )

    for label, requests in data.items():
        # Count total requests out
        domains = defaultdict(int)
        for request in requests:
            domains[request["host"]] += 1

        # Add label node
        hover_text = "<b>Domains:</b>"
        for domain, count in sorted(
            domains.items(), key=lambda kv: kv[1], reverse=True
        ):
            hover_text += f"<br>{domain} - {count}"
        network.add_node(
            label, label=label, shape="circle", group=label, title=hover_text
        )

        # Add edges
        for domain, count in domains.items():
            network.add_edge(label, domain, title=str(count), value=count)

    # Create network graph
    network.force_atlas_2based(
        gravity=-155,
        central_gravity=0.035,
        spring_length=70,
        spring_strength=0.215,
        damping=0.55,
        overlap=1,
    )
    # network.show_buttons(["physics"])
    network.toggle_physics(True)
    network.show(f"{name}.html")


if __name__ == "__main__":
    filepath = sys.argv[1]
    with open(filepath) as file:
        data = json.load(file)
    name = os.path.basename(filepath).replace(".json", "")
    main(data, name)
