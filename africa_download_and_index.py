import datetime
import requests
import es

ACLED_URL = "https://api.acleddata.com/acled/read"


def hydrate_event(event):
    """
    Add reelevant/contextual info to the event dict
    :param event:
    :return:
    """
    event["id"] = event["data_id"]
    event["@timestamp"] = event["event_date"]
    event["location_name"] = event["location"]
    event["location"] = {"lat": event["latitude"], "lon": event["longitude"]}
    event["zone"] = "africa"
    return event


def download():
    """

    :return:
    """
    years = range(1997, datetime.date.today().year + 1)

    print datetime.datetime.today(), "- downloading data for years:", years

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
            events = data['data']
            print "indexing on", es.ES_ACLED_INDEX, "..."

            for event in events:
                event = hydrate_event(event)
                es.index(event)

            page += 1
            if data['count'] < 500:
                paginate = False


if __name__ == "__main__":
    download()
