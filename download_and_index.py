import json
import os
import datetime
import requests
from requests.auth import HTTPBasicAuth

ACLED_URL = "https://api.acleddata.com/acled/read"
ES_HOST = os.environ.get("ES_HOST")
ES_USER = os.environ.get("ES_USER")
ES_PASSWORD = os.environ.get("ES_PASSWORD")
ES_ACLED_INDEX = os.environ.get("ES_ACLED_INDEX")
URL = ES_HOST + ES_ACLED_INDEX + "/event"

def index(data):
    for event in data:
        event["id"] = event["data_id"]
        event["@timestamp"] = event["event_date"]
        event["location_name"] = event["location"]
        event["location"] = {"lat": event["latitude"], "lon": event["longitude"]}

        res = requests.post(URL, json=event, auth=HTTPBasicAuth(ES_USER, ES_PASSWORD))

def download():
    years = range(1997, datetime.date.today().year + 1)

    print "downloading data for years:", years

    for year in years:
        paginate = True
        page = 1
        while paginate:
            params = {
                "year": year,
                "page": page
            }

            print "downloading", year, "page", page
            res = requests.get(ACLED_URL, params=params)
            data = res.json()

            print "indexing on", ES_ACLED_INDEX, "..."
            index(data['data'])

            page += 1
            if data['count'] < 500:
                paginate = False


if __name__ == "__main__":
    download()
