# Collect Twitter 

[![N|Solid](http://www.labic.net/wp-content/themes/labicv16/assets/logo-lg.png)](http://www.labic.net/)

# New Features!
  - send to elasticSearch

### Installation
requires [Python](https://www.python.org/) 2.7 to run.

Install the dependencies and devDependencies and start the service.

```sh
$ git clone  https://github.com/andreibastos/colect-stream-twitter.git
$ cd colect-stream-twitter
$ virtualenv . 
$ source bin/activate
```
install dependencies
```sh
$ pip install -r requirements.txt
$ 
```

For production configs...

First: edit file config.json
```sh
$ nano config.json
```
```json
{
    "collector":{
        "NUM_PER_INSERT":25,
        "categorize_namefield":"categories",
        "sendTelegram":true,
        "chat_id": 999999
    },

    "endpoints":{
        "api_database" : "http://your_api",
        "api_bot_telegram" : "http://your_bot_telegram",
        "api_categorize" : "http://your_api_categorize",
        "api_categorize2" : "http://your_api_categorize"
    },
    "files":{
        "filename_log" : "clipper.log",
        "filename_keys" : "keys.json",
        "filename_querys" : "querys.json"
    }

}
```

Second: edit file keys.json
```sh
$ nano keys.json
```
```json

[
    ["hmUbVS0OEqLMPNUdvpDp3nF9k", "mXmj4ZxMcKNUc9nF8wF8aOUf0KeVGWLTXeBUrtptx55Cj6JwLV", "70141627-IbOIyGNpKgEtMg6dhU84onqyOHodPMOCJ6HUaUKaT", "uus0nbmPprAErWyvXtmxxQXaiSNZEzZImqMOuJo3bMDHO"]
]

```
Order: [consumer_key, consumer_secret, access_token, access_token_secret]

third: edit file querys.json
```sh
$ nano querys.json
```
```json
[
    {
        "track": [
            "oculos"             
        ], 
        "languages": [
            "pt"
        ]
    }
]
```
### Run
```sh
$ source bin/activate
$ export ES_HOST_URI_00='localhost:9200' && python2.7 coletor.py
```
### Stop
```sh
CTRL-C
```
