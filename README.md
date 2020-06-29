# Search Engine for Sinhala Songs #

## Quickstart ##
* Start elasticsearch on port 9200
* Run the command python3 run.py
* Visit localhost:5000
* Enter the search phrase in the search box

## Technology used ##
* Elasticsearch 7.7.1
* Elasticsearch DSL 7.2.0
* Python 3.6.3
* Flask 1.1.2
* Scrapy 2.1.0

## Directory Structure ##
    |-- app
       |-- templtes   : UI files
       |-- app.py     : flask backend
       |-- search.py  : elasticsearch queries
    |-- songs_scraper : scripts to scrape lyrics and metadata from https://sinhalasongbook.com/
       |-- songs.json : scrapped data
    |-- constants.py  : index_name and doc_type as constants
    |-- run.py        : start the search engine

## Main Functionalities ##

* Faceted search
* Range queries
* Advance search
* Partial query support

## Corpus ##
Scraped https://sinhalasongbook.com/ to get lyrics and meta-data for 500 Sinhala songs

* Meta-data scrapped
    * Artist
    * Lyric writer
    * Composer
    * Song title
    * Genre
    * Beat
    * Key
    * Number of views

## Supported Queries (examples) ##
* මිල්ටන් ගැයූ ගී
* ප්රේමකීර්ති ලියපු සින්දු
* ප්රේමකීර්ති ලියු ජනප්‍රිය ගීත 10 ක්
* ප්‍රසිද්ධ සම්භාව්ය ගීත
* කපුගේ කියන සම්භාව්ය ගීත
