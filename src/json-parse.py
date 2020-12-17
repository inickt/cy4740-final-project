import json
import sys
def main():
    hosts= {}

    f= open('cnn.json')
    data= json.load(f)

    # Pass name of json dump as command line argument
    for i in data[sys.argv[1]]:
        for j in i['host']:
            #print(i['host'])            
            if i['host'] in hosts:
                hosts[i['host']]= hosts[i['host']] + 1
            else:
                hosts[i['host']]= 1

    with open('parsed.json', 'w') as out:
        json.dump(hosts, out)

    #print(hosts)
    f.close()

main()