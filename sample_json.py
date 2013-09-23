#!/usr/bin/env python        

import json
from pprint import pprint

with open('LocationHistory.json') as data_file:    
    data = json.load(data_file)
for location in data['locations']:
	print location['latitudeE7']
