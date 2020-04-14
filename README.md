# ZotBins Temporary API
This API is hosted by pythonanywhere.com and the following requests are currently available:

## Table of Contents
1. [Add Observation](#add-observation)
2. [Get Observation](#get-observation)
3. [Count Observation](#count-observation)
3. [Add Barcode](#add-barcode)
4. [Get Barcode](#get-barcode)
5. [Add Image](#add-image)

### Add Observation
Endpoint: base URL + /observation/add \
Method: POST\
Body example:
```json
[
    {
        "timestamp": "2020-02-01 9:30:01",
        "payload":
        {
            "weight": 100
        },
        "sensor_id": "ZBin2",
        "type": 2
    }
]
```
Description:
* Adds new observation(s) to the database, currently takes 3 different observation types (2=weight, 3=distance, 5=frequency)


### Get Observation
Endpoint: base URL + /observation/get \
Method: GET \
Params:
- sensor_id
- start_timestamp
- end_timestamp

Description:
* Fetches observation(s) recorded by a sensor within a specific timeframe
* Sensor ID # can be found in our Google drive > NOTES-Milestones-Tasks > ZotBinsID Tracker
* Sensor ID format = "ZBin" + sensor ID # + ("B" if breakbeam sensor, "D" if ultrasonic sensor)

### Count Observation
Endpoint: base URL + /observation/count \
Method: GET \
Params:
- sensor_id
- start_timestamp
- end_timestamp

Description:
* Fetches a sum for the observation(s) recorded by a sensor within a specific timeframe
* Sensor ID # can be found in our Google drive > NOTES-Milestones-Tasks > ZotBinsID Tracker
* Sensor ID format = "ZBin" + sensor ID # + ("B" if breakbeam sensor, "D" if ultrasonic sensor)

### Add Barcode
Endpoint: base URL + /barcode/add \
Method: POST\
Body example:
```json
[
    {
        "name": "Fiji Water Bottle",
        "type": "water bottle",
        "barcode": 123456789012,
        "wasteBin": "recycling",
        "instructions": "Wrapper and cap in landfill, bottle in recycling"
    }
]
```
Description: Adds new barcodes(s) to the database

### Get Barcode
Endpoint: base URL + /barcode/get \
Method: GET \
Body example:
```json
[
    {
        "barcode": 123456789012
    }
]
```

Description: Get the item, item type, and instructions on how to properly dispose of it

### Add Image
Endpoint: base URL + /image/add \
Method:
Body example:
```python
import requests
import json

url = "BASE_URL/image/add"

with open(YOUR_FILE_PATH, 'rb') as f:
    r = requests.post(url, files={"file": f})
```

Description: Adds an image to the filesystem. The purpose of the images is to collect waste related data. You can also interact with the HTML UI to post an image on `base URL + /image/add`


#### Additional info:
* This API is the same format as the [old TIPPERS API](https://zotbins.github.io/tippersdocs/doc/index.html#api-Observation-AddObservation)
  * Checkout the postman collection file in this repo (ZotBinsAPI.postman_collection.json) for request examples.
* ZotBinsAPI.py is the script that runs the flask app which acts as a middle man between user (us) and the database.
  * It requires two extra files that aren't included in this repo: config.py (contains db info) and queries.py (contains sql queries)
