from collections import defaultdict
import json
import sys


def main(filenames):
    data = defaultdict(list)
    for filename in filenames:
        with open(filename) as file:
            file_dump = json.load(file)
            for label, requests in file_dump.items():
                data[label].extend(requests)
    with open("merged.json", "w") as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    filenames = sys.argv[1::]
    print(filenames)
    main(filenames)