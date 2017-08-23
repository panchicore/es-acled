import requests
import es
from requests.auth import HTTPBasicAuth


def create_indice(delete=None):
    """

    :param delete:
    :return:
    """

    if delete:
        requests.delete(es.URL, auth=HTTPBasicAuth(es.ES_USER, es.ES_PASSWORD))

    template = open("elasticsearch/acled-template.json").read()
    res = requests.put(es.URL, data=template, auth=HTTPBasicAuth(es.ES_USER, es.ES_PASSWORD))

    print res.content


if __name__ == "__main__":
    delete = raw_input("Want to delete the actual '{0}' index? Y/N: ".format(es.ES_ACLED_INDEX)) == "Y"
    create_indice(delete)
