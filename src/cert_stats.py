from collections import defaultdict
import json
import sys


def main(data):
    overall_issuer_count = defaultdict(int)
    for label in data:
        print(f"{label}:\n{'-' * 50}")
        issuer_count = defaultdict(int)
        for request in data[label]:
            if request["cert"] is not None:
                org = request["cert"]["issuer"].get("O") or "Unknown"
                issuer_count[org] += 1
                overall_issuer_count[org] += 1
            else:
                issuer_count[None] += 1
                overall_issuer_count[None] += 1
        total = sum(issuer_count.values())
        for issuer, count in sorted(
            issuer_count.items(), key=lambda kv: kv[1], reverse=True
        ):
            percent = (float(count) / total) * 100
            print(f"  {issuer or 'No TLS'} - {count} - {percent:.2f}%")
        print()

    overall_total = sum(overall_issuer_count.values())
    print(f"Overall totals:\n{'-' * 50}")
    for issuer, count in sorted(
        overall_issuer_count.items(), key=lambda kv: kv[1], reverse=True
    ):
        percent = (float(count) / overall_total) * 100
        print(f"  {issuer or 'No TLS'} - {count} - {percent:.2f}%")


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        data = json.load(f)
    main(data)
