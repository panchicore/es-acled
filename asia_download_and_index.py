import os
import re

import es
from urllib import urlretrieve

import requests
from bs4 import BeautifulSoup
from xlrd import open_workbook, xldate_as_tuple

ACLED_ASIA_URL = "http://www.acleddata.com/asia-data/"


def start():
    res = requests.get(ACLED_ASIA_URL)
    soup = BeautifulSoup(res.content, "html.parser")
    download_links = []
    events = []

    for link in soup.find_all('a'):
        if link.get('href').lower().count("ACLED-Asia-Running-File".lower()) > 0:
            download_links.append(link.get('href'))

    for link in download_links:
        print "downloading", link
        file_name = link.split("/")[-1]
        file_path = os.path.join("data", "asia", file_name)
        urlretrieve(link, file_path)
        print "extracting", file_path

        wb = open_workbook(file_path)
        s = wb.sheet_by_index(0)

        for r in range(1, s.nrows):
            GWNO = s.row(r)[0].value
            EVENT_ID_CNTY = s.row(r)[1].value
            EVENT_ID_NO_CNTY = s.row(r)[2].value
            EVENT_DATE = xldate_as_tuple(s.row(r)[3].value, wb.datemode)
            EVENT_DATE = "{0}-{1}-{2}".format(EVENT_DATE[0], EVENT_DATE[1], EVENT_DATE[2])
            YEAR = int(s.row(r)[4].value)
            TIME_PRECISION = s.row(r)[5].value
            EVENT_TYPE = s.row(r)[6].value
            ACTOR1 = s.row(r)[7].value
            ALLY_ACTOR_1 = s.row(r)[8].value
            INTER1 = s.row(r)[9].value
            ACTOR2 = s.row(r)[10].value
            ALLY_ACTOR_2 = s.row(r)[11].value
            INTER2 = s.row(r)[12].value
            INTERACTION = s.row(r)[13].value
            COUNTRY = s.row(r)[14].value
            ADMIN1 = s.row(r)[15].value
            ADMIN2 = s.row(r)[16].value
            ADMIN3 = s.row(r)[17].value
            LOCATION = s.row(r)[18].value
            LATITUDE = s.row(r)[19].value
            LONGITUDE = s.row(r)[20].value
            GEO_PRECISION = s.row(r)[21].value
            SOURCE = s.row(r)[22].value
            NOTES = s.row(r)[23].value
            FATALITIES = s.row(r)[24].value

            ID = "{0}.{1}.{2}.{3}".format(
                YEAR, GWNO, EVENT_ID_CNTY, EVENT_ID_NO_CNTY
            )

            event = {
                'id': ID,
                '@timestamp': EVENT_DATE,
                'actor1': ACTOR1,
                'actor2': ACTOR2,
                'admin1': ADMIN1,
                'admin2': ADMIN2,
                'admin3': ADMIN3,
                'ally_actor_1': ALLY_ACTOR_1,
                'ally_actor_2': ALLY_ACTOR_2,
                'country': COUNTRY,
                'data_id': ID,
                'event_date': EVENT_DATE,
                'event_id_cnty': EVENT_ID_CNTY,
                'event_id_no_cnty': EVENT_ID_NO_CNTY,
                'event_type': EVENT_TYPE,
                'fatalities': FATALITIES,
                'geo_precision': GEO_PRECISION,
                'gwno': GWNO,
                'inter1': INTER1,
                'inter2': INTER2,
                'interaction': INTERACTION,
                'location_name': LOCATION,
                'notes': NOTES,
                'source': SOURCE,
                'time_precision': TIME_PRECISION,
                'year': YEAR,
                'latitude': LATITUDE,
                'longitude': LONGITUDE,
                'zone': 'asia',
                'file_path': file_path,
                'file_link': link
            }

            # fix coordinates, xls sometimes brings bad encoding chars
            if type(LATITUDE) is not float:
                LATITUDE = re.findall("\d+\.\d+", LATITUDE or "")
                if LATITUDE and LATITUDE[0]:
                    event['latitude'] = float(LATITUDE[0])

            if type(LONGITUDE) is not float:
                LONGITUDE = re.findall("\d+\.\d+", LONGITUDE or "")
                if LONGITUDE and LONGITUDE[0]:
                    event['longitude'] = float(LONGITUDE[0])

            event['location'] = {
                "lat": event['latitude'],
                "lon": event['longitude']
            }

            events.append(event)

    print "indexing", len(events), "events..."
    for event in events:
        es.index(event)


if __name__ == "__main__":
    start()
