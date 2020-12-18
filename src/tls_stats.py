from collections import defaultdict
import json
import sys


def main(data):
    overall_tls_count = defaultdict(int)
    for label in data:
        print(f"{label}:\n{'-' * 50}")
        tls_count = defaultdict(int)
        for request in data[label]:
            tls_count[request["tls_version"]] += 1
            overall_tls_count[request["tls_version"]] += 1
        total = sum(tls_count.values())
        for tls_type, count in sorted(
            tls_count.items(), key=lambda kv: kv[1], reverse=True
        ):
            percent = (float(count) / total) * 100
            print(f"  {tls_type or 'No TLS'} - {count} - {percent:.2f}%")
        print()

    overall_total = sum(overall_tls_count.values())
    print(f"Overall totals:\n{'-' * 50}")
    for tls_type, count in sorted(
        overall_tls_count.items(), key=lambda kv: kv[1], reverse=True
    ):
        percent = (float(count) / overall_total) * 100
        print(f"  {tls_type or 'No TLS'} - {count} - {percent:.2f}%")


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        data = json.load(f)
    main(data)
