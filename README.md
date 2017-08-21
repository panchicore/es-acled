# es-acled
Elastic search index for the `Armed Conflict Location and Event Data Project (ACLED)`

## Setup
1. check the environment vars at `config/enviroment_variables.sample.sh`
2. for now this project requires `requests`, install with `pip install `config/requirements.txt`
3. create index with `python create_index.py`
4. download the data since 1997 and index it on ES with `python download_and_index.py` this will download the data until the current year.
5. to keep index up-to-date a cronjob will be required.

## Contribute
Please fork this repo.

## Todo
1. real time update (each 24 hrs with cronjob)