#! /usr/bin/env python3
import requests
import json
from halo import Halo
from log_symbols import LogSymbols
from bs4 import BeautifulSoup as bs

# Fetch icon cheatsheet page
try:
    url = "https://ionic.io/ionicons/v2/cheatsheet.html"
    response = requests.get(url)
    html = response.content
    print(LogSymbols.SUCCESS.value, "Icon Cheatsheet")
except requests.exceptions.RequestException as e:  # This is the correct syntax
    raise SystemExit(e)

# Scrape icon names from page
soup = bs(html, 'html.parser')
all_icons = soup.select("input.name")
print(LogSymbols.SUCCESS.value, "Icons:", len(all_icons))

# PUT the node appearances
nodeAppearances = [{"predicate":{"propertyKeys":[],"knownValues":{},"dbLabel": icon_name["value"].replace("-", "_")},"size":40.0,"icon": icon_name["value"]} for icon_name in all_icons]
json_data = json.dumps(nodeAppearances)
try:
    headers = {'Content-type': 'application/json'}
    response = requests.put('http://localhost:8080/api/v1/query-ui/node-appearances', data=json_data, headers=headers)
except requests.exceptions.RequestException as e:  
    raise SystemExit(e)

# POST icon nodes to decorate
quineSpinner = Halo(text='Creating Icon Nodes', spinner='bouncingBar')
try:
    quineSpinner.start()
    for icon_name in all_icons:
        query_text = 'CREATE (n:' + icon_name["value"].replace("-", "_") + ')'
        quineSpinner.text = query_text
        headers = {'Content-type': 'text/plain'}
        response = requests.post('http://localhost:8080/api/v1/query/cypher', data=query_text, headers=headers)
    quineSpinner.succeed('Icon Nodes')
except requests.exceptions.Timeout as timeout:
    quineSpinner.stop('Request Timeout: ' + timeout)
except requests.exceptions.RequestException as e:
    raise SystemExit(e)
