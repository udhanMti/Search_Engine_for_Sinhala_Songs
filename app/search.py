from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from searchapp.constants import DOC_TYPE, INDEX_NAME

HEADERS = {'content-type': 'application/json'}

#basic query with boosted fields and aggregations
def do_general_search(term,fields):
    client = Elasticsearch()
    client.transport.connection_pool.connection.headers.update(HEADERS)

    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE).extra(size=450)
    query = {
    "multi_match": {
				"query": term,
				"fields": fields,
				"operator": 'or',
				"type": "best_fields"
	            }
    }
    s.aggs.bucket('ගායනය', 'terms', field='Artist.keyword', size=10)
    s.aggs.bucket('පද රචනය', 'terms', field='Lyrics.keyword', size=10)
    s.aggs.bucket('සංගීතය', 'terms', field='Music.keyword', size=10)
    s.aggs.bucket('ශානරය', 'terms', field='Genre.keyword', size=10)
    docs=s.query(query).execute()

    return docs

#query with boosted fields and aggregations and sorted with number of views
def do_general_range_search(term, count, fields):
    client = Elasticsearch()
    client.transport.connection_pool.connection.headers.update(HEADERS)

    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE)
    query = {
            "multi_match": {
                "query": term,
                "fields": fields,
                "operator": 'or'
            }
    }

    docs = s.query(query).sort({'Views': {'order': "desc"}})[:count].execute()

    return docs

#query for advanced search
def do_advanced_search(body, artist, lyrics, music, genre, count):
    client = Elasticsearch()
    client.transport.connection_pool.connection.headers.update(HEADERS)

    list_of_fields=[]
    if(artist!=''):
        list_of_fields.append({"match": {"Artist": artist,}})
    if(lyrics!=''):
        list_of_fields.append({"match": {"Lyrics": lyrics,}})
    if(music!=''):
        list_of_fields.append({"match": {"Music": music,}})
    if(genre!=''):
        list_of_fields.append({"match": {"Genre": genre,}})
    if(body!=''):
        list_of_fields.append({"match": {"Body": body,}})
    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE).extra(size=450)
    query = {
            "bool": {
                "must": list_of_fields
            }
        }
    s.aggs.bucket('ගායනය', 'terms', field='Artist.keyword', size=10)
    s.aggs.bucket('පද රචනය', 'terms', field='Lyrics.keyword', size=10)
    s.aggs.bucket('සංගීතය', 'terms', field='Music.keyword', size=10)
    s.aggs.bucket('ශානරය', 'terms', field='Genre.keyword', size=10)
    docs = s.query(query)[:count].execute()

    return docs