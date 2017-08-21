import datetime
import requests
from africa_download_and_index import index, ACLED_URL, ES_ACLED_INDEX


def download():
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

        print "indexing on", ES_ACLED_INDEX, "..."
        index(data['data'])

        page += 1
        if data['count'] < 500:
            paginate = False


if __name__ == "__main__":
    download()
