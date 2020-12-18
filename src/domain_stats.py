from collections import defaultdict
import json
import sys


def main(data):
    overall_domains = defaultdict(int)
    for label, requests in data.items():
        domains = defaultdict(int)
        for request in requests:
            domains[request["host"]] += 1
            overall_domains[request["host"]] += 1
        total = sum(domains.values())
        print(f"{label} ({total}):\n{'-' * 50}")
        for domain, count in sorted(
            domains.items(), key=lambda kv: kv[1], reverse=True
        ):
            print(f"  {count} - {domain}")
        print()

    overall_total = sum(domains.values())
    print(f"Overall totals ({overall_total}):\n{'-' * 50}")
    for domain, count in sorted(
        overall_domains.items(), key=lambda kv: kv[1], reverse=True
    ):
        print(f"  {count} - {domain}")

    print(f"\nCross usage totals:\n{'-' * 50}")
    sites = defaultdict(list)
    for domain in overall_domains:
        for label, requests in data.items():
            for request in requests:
                if request["host"] == domain:
                    sites[domain].append(label)
                    break
    for domain, sites in sorted(sites.items(), key=lambda kv: len(kv[1]), reverse=True):
        if len(sites) > 1:
            print(f"  {len(sites)} - {domain} - ({', '.join(sites)})")


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        data = json.load(f)
    main(data)