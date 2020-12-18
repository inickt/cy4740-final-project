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


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        data = json.load(f)
    main(data)