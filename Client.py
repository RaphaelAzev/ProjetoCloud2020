import json
import requests
import datetime
import sys

with open('LoadDNS.txt', 'r') as arq:
    my_url = arq.readline()

#my_url = 'http://3.88.142.177:8080/tasks'

#print(url)

if sys.argv[1] == 'getAll':
    r = requests.get(url=my_url + "/alltasks")
    print(json.dumps(r.json()))

if sys.argv[1] == 'postTask':
    date = str(datetime.datetime.now())
    title = input('Title da task: ')
    description = input('Descricao da task: ')
    jsonfile = {
        "title": title,
        "pub_date": date,
        "description": description
    }
    r = requests.post(url=my_url + "/posttask",json=jsonfile)
    
