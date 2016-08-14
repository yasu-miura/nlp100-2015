# coding:utf-8
from pymongo import MongoClient
from contextlib import contextmanager


@contextmanager
def get_connection():
    try:
        client = MongoClient('localhost', 27017)
        yield client
    except Exception as e:
        print("with an error (%s)" % e)
        raise e
    finally:
        client.close()


def get_artists_by_name(name):
    with get_connection() as client:
        artists = client.artists.artists
        results = artists.find({"name": name})
    return results


def get_artists_by_another_name(another_name):
    with get_connection() as client:
        artists = client.artists.artists
        results = artists.find({"aliases.name": another_name})
    return results


def get_artists_by_name_and_another_name(name, another_name):
    with get_connection() as client:
        artists = client.artists.artists
        results = artists.find({"name": name,"aliases.name": another_name})
    return results
