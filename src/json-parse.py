import json
import sys

# Renamed the dump file to the same name as the filter I used for simplicity

def main():
    hosts= {}

    f= open(sys.argv[1]+'.json')
    data= json.load(f)

    # Pass name of json dump as command line argument
    for i in data[sys.argv[1]]:
        if i['host'] in hosts:
            hosts[i['host']]= hosts[i['host']] + 1
        else:
            hosts[i['host']]= 1

    with open(sys.argv[1]+'_parsed.json', 'w') as out:
        json.dump(hosts, out)

    f.close()

main()