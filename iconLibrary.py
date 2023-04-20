#! /usr/bin/env python3
import requests
import json
from halo import Halo
from log_symbols import LogSymbols
from bs4 import BeautifulSoup

# Fetch icon cheatsheet page
try:
    url = "https://ionic.io/ionicons/v2/cheatsheet.html"
    response = requests.get(url)
    html = response.content
    print(LogSymbols.SUCCESS.value, "GET Icon Cheatsheet")
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

# Extract icon names from page
soup = BeautifulSoup(html, 'html.parser')
all_icons = soup.select("input.name")
print(LogSymbols.SUCCESS.value, "Extract Icon Names:", len(all_icons))

# PUT the node appearances
nodeAppearances = [
    {
        "predicate": {
            "propertyKeys": [],
            "knownValues": {},
            "dbLabel": icon_name["value"].replace("-", "_")
        },
        "size":40.0,
        "icon": icon_name["value"],
        "label": {
            "key": "name",
            "type": "Property"
        }
    } for icon_name in all_icons]
json_data = json.dumps(nodeAppearances)
try:
    headers = {'Content-type': 'application/json'}
    response = requests.put(
        'http://localhost:8080/api/v1/query-ui/node-appearances', data=json_data, headers=headers)
except requests.exceptions.RequestException as e:
    raise SystemExit(e)
print(LogSymbols.SUCCESS.value, "PUT Node Appearances")

# POST icon nodes to decorate
quineSpinner = Halo(text='Creating Icon Nodes', spinner='bouncingBar')
try:
    quineSpinner.start()
    for icon_name in all_icons:
        group = icon_name["value"].split('-',2)
        query_text = (
            f'MATCH (a), (b), (c) '
            f'WHERE id(a) = idFrom("{group[0]}") '
            f'  AND id(b) = idFrom("{group[1]}") '
            f'  AND id(c) = idFrom("{icon_name["value"]}") '
            f'SET a:{group[0]}, a.name = "{group[0]}" '
            f'SET b:{group[1]}, b.name = "{group[1]}" '
            f'SET c:{icon_name["value"].replace("-", "_")}, c.name = "{icon_name["value"]}" '
            f'CREATE (a)<-[:` `]-(b)<-[:` `]-(c)'
          ) if len(group) == 3 else (
            f'MATCH (a), (c) '
            f'WHERE id(a) = idFrom("{group[0]}") '
            f' AND id(c) = idFrom("{icon_name["value"]}") '
            f'SET a:{group[0]}, a.name = "{group[0]}" '
            f'SET c:{icon_name["value"].replace("-", "_")}, c.name = "{icon_name["value"]}" '
            f'CREATE (a)<-[:` `]-(c)'
          )
        quineSpinner.text = query_text
        headers = {'Content-type': 'text/plain'}
        # print(query_text)
        response = requests.post(
            'http://localhost:8080/api/v1/query/cypher', data=query_text, headers=headers)
    quineSpinner.succeed('POST Icon Nodes')
except requests.exceptions.Timeout as timeout:
    quineSpinner.stop('Request Timeout: ' + timeout)
except requests.exceptions.RequestException as e:
    raise SystemExit(e)
