import os
import requests


#Get fdp uri from node envir variable
station_uri = os.environ.get("DATABASE_URI")
if station_uri is None:
    station_uri = "http://localhost:5000"
else:
    station_uri = str(station_uri)

print("station_uri :" + station_uri)

# Read train requirement
train_metadata = open('train-metadata.ttl', 'r').read()

# Get datasets matches the conditions
url = station_uri + "/getDataset"
response = requests.post(url,data = train_metadata)
output = response.text

print(output)
# Write query result to output file
with open('output.txt', 'w') as f:
    f.write(str(output))

