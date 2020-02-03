# ZotBinsAPI
This API is hosted by pythonanywhere.com and the following requests are currently available:

### Add Observation
URL: https://zotbins.pythonanywhere.com/observation/add \
Method: POST\
Body example:     \
```json
[
   {
    "timestamp": "2019-12-05 9:30:01",
    "payload": {
        "weight": 100
    },
    "sensor_id": "zbin1",
    "type": 2
  }
]
```
Description: Adds new observation(s) to the database, currently takes 3 different observation types \
              (2=weight, 3=distance, 5=frequency)


### Get Observation
URL: https://zotbins.pythonanywhere.com/observation/get \
Method: GET\
Body example:
```json
{
	"sensor_id": "zbin1",
	"start_timestamp": "2019-12-02 9:30:01",
	"end_timestamp": "2019-12-06 9:30:01"
}
```
Description:
* Fetches observation(s) recorded by specific sensor ID and timeframe
* Sensor ID # can be found in our Google drive > NOTES-Milestones-Tasks > ZotBinsID Tracker
* Sensor ID format = "ZBin" + sensor ID # + ("B" if breakbeam sensor, "D" if ultrasonic sensor)
              
Other info:\
This API is the same format as the [old TIPPERS API](https://zotbins.github.io/tippersdocs/doc/index.html#api-Observation-AddObservation) \
\
Checkout the postman collection file in this repo (ZotBinsAPI.postman_collection.json) for request examples.\
\
ZotBinsAPI.py is the script that runs the flask app which acts as a middle man between user (us) and the database.\
It requires two extra files that aren't included in this repo: config.py (contains db info) and queries.py (contains sql queries)\

