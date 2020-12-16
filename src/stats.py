
from collections import defaultdict
import json, sys

def main(data):
    for label in data:
        tls_count = defaultdict(int)
        for request in data[label]:
            tls_count[request['tls_version']] += 1
        for tls_type in tls_count:
            print(f"Label --> {label} --> TLS_TYPE --> {tls_type} --> NUMBER OF TLS_CONNECTIONS --> {tls_count[tls_type]}")
        print("")


if __name__ == '__main__':
    json_data = sys.argv[1]
    with open(json_data) as f:
        data = json.load(f)

    main(data)
    