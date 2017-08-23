import datetime
import requests
import es
from africa_download_and_index import ACLED_URL, hydrate_event


def download():
    """

    :return:
    """
    year = datetime.date.today().year
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

        print "indexing on", es.ES_ACLED_INDEX, "..."
        for event in data['data']:
            event = hydrate_event(event)
            es.index(event)

        page += 1
        if data['count'] < 500:
            paginate = False


if __name__ == "__main__":
    download()
