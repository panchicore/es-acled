# es-acled
Elastic search index for the `Armed Conflict Location and Event Data Project (ACLED)` from Asia and Africa in the same Elastic Search index.

## Setup
1. check the environment vars at `config/enviroment_variables.sample.sh`
2. install python requirements with `pip install config/requirements.txt`
3. create index with `python create_index.py`
4. download the Africa data since 1997 and index it on ES with `python download_and_index.py` this will download the data until the current year.

## Realtime updates
To keep index up-to-date a cron job will be required with the following commands:

#### Africa data
API Client for all events from current year
```
python africa_realtime.py
```

#### Asia data
Crawler for published excels in here (http://www.acleddata.com/asia-data/)
```
python asia_download_and_index.py
```


## Contribute
Please fork this repo.

## Todo
1. ~~Real time updates~~
2. Unit tests