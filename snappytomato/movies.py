#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from .api import API
from .utils import normalize_text, attach_attributes
from collections import Counter


class MoviesAPI(API):
    """
    Interface to rottentomatoes search api

    See http://developer.rottentomatoes.com/io-docs
    """

    LISTS = "/lists/movies"
    def __init__(self, api_key):
        super(MoviesAPI, self).__init__(api_key)

    def _get_movies_json(self, url, payload):
        return self._GET(url, payload).get("movies", None)

    def _movies_from_json(self, jdata):
        return [Movie(entry["id"], self, entry) for entry in jdata]

    def _box_office(self, **kwargs):
        jdata = payload = self._build_payload(kwargs)
        url = "{}{}/box_office.json".format(self._base_url, MoviesAPI.LISTS)
        return self._get_movies_json(url, payload)

    def box_office(self, **kwargs):
        jdata = self._box_office(**kwargs)
        return self._movies_from_json(jdata)

    def _in_theaters(self, **kwargs):
        payload = self._build_payload(kwargs)
        url = "{}{}/in_theaters.json".format(self._base_url, MoviesAPI.LISTS)
        return self._get_movies_json(url, payload)

    def in_theaters(self, **kwargs):
        jdata = self._in_theaters(**kwargs)
        return self._movies_from_json(jdata)

    def _opening(self, **kwargs):
        payload = self._build_payload(kwargs)
        url = "{}{}/opening.json".format(self._base_url, MoviesAPI.LISTS)
        return self._get_movies_json(url, payload)

    def opening(self, **kwargs):
        jdata = self._opening(**kwargs)
        return self._movies_from_json(jdata)

    def _upcoming(self, **kwargs):
        payload = self._build_payload(kwargs)
        url = "{}{}/upcoming.json".format(self._base_url, MoviesAPI.LISTS)
        return self._get_movies_json(url, payload)

    def upcoming(self, **kwargs):
        jdata = self._upcoming(**kwargs)
        return self._movies_from_json(jdata)

    def _search(self, query, **kwargs):
        """
        Search for movies matching terms

        returns a JSON dict (response from request)
        """
        kwargs["q"] = query
        payload = self._build_payload(kwargs)
        url = "{}/movies.json".format(self._base_url)
        return self._get_movies_json(url, payload)

    def search(self, query, **kwargs):
        """
        Search for movies matching terms

        returns a list of Movies
        """
        jdata = self._search(query, **kwargs)
        return self._movies_from_json(jdata)

    def movie_by_id(self, movie_id):
        return Movie(movie_id, self, entry_for_movie_id(movie_id))

    def movie_by_title(self, title):
        movies = self._search(query=title)
        normalized_title = normalize_text(title)
        for entry in movies:
            if normalized_title == normalize_text(entry["title"]):
                return Movie(entry["id"], self, entry)
        return None

    def entry_for_movie_id(self, movie_id):
        """
        Retrieve rottentomatoes JSON for movie.

        returns a JSON dict (response from request)
        """
        payload = mapi.payload
        url = "{}/movies/{}.json".format(mapi._base_url, movie_id)
        return mapi._GET(url, payload)

class Movie(object):
    """
    Storage class for rottentomatoes movie data
    """
    def __init__(self, movie_id, mapi, movie_data=dict()):
        self.id = movie_id
        self._mapi = mapi
        # most of the work is done here
        attach_attributes(self, movie_data or self._mapi.entry_for_movie_id(self.id))
        # the uri for this movie's json
        self._address = self.links["self"]
        # make the "reviews" and "cast" attributes easier to access
        self.reviews = self._get_reviews()
        self.cast = self._mapi._retrieve_rt_json(self.links["cast"]) if "cast" in self.links else None
        # convient access to ratings
        attach_attributes(self, movie_data.get("ratings"))
        # count rt freshness
        self.freshness = Counter([r.freshness for r in self.reviews]) if self.reviews else None

    def __str__(self):
        name = self.__class__.__name__
        return "{}(\"{}\", {})".format(name, self.title, self._address)

    def _get_reviews(self):
        if "reviews" in self.links:
            reviews_json = self._mapi._retrieve_rt_json(self.links["reviews"])
            reviews = reviews_json.get("reviews", None)
            return [Review(self, **jdata) for jdata in reviews] if reviews else None
        return None

    def similar(self):
        """Retrieve similar movies (according to rottentomatoes)

        builds a similarity graph constructed on-the-fly using a generator
        """
        if "similar" in self.links:
            reviews_json = self._mapi._retrieve_rt_json(self.links["similar"])
            movies = reviews_json.get("movies", None)
            # build a similarity graph
            return (Movie(jdata["id"], self._mapi, jdata) for jdata in movies) if movies else None
        return None

class Review(object):
    """
    Storage class for rottentomatoes review data
    """
    def __init__(self, movie, **kwargs):
        self.movie = movie
        attach_attributes(self, kwargs)
        self.source = kwargs["links"].get('review', None)
        # self.critic = critic
        # self.date = date
        # self.freshness = freshness
        # TODO: would be fun to normalize this (ex. "4/4" -> 1.0 3 "3 out of 4 stars" -> .75, etc.)
        # self.original_score
        # self.publication
        # self.quote

    def __str__(self):
        name = self.__class__.__name__
        return "{}({}, \"{}\")".format(name, self.critic, self.movie.title)
