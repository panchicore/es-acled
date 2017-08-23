import os
import requests
from requests.auth import HTTPBasicAuth

ES_HOST = os.environ.get("ES_ACLED_HOST")
ES_USER = os.environ.get("ES_ACLED_USER")
ES_PASSWORD = os.environ.get("ES_ACLED_PASSWORD")
ES_ACLED_INDEX = os.environ.get("ES_ACLED_INDEX")
URL = ES_HOST + ES_ACLED_INDEX
INDEX_URL = URL + "/event/"


def index(event):
    """
    Send data to Elastic Search host.
    :param data: ACLED record
    :return:
    """

    res = requests.post(INDEX_URL + event['id'], json=event, auth=HTTPBasicAuth(ES_USER, ES_PASSWORD))
    if not res.ok:
        print event
        print res, res.content
        print '------'