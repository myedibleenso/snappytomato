#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import requests
import json
import os

API_KEY = os.environ.get("RT_KEY", None)

class API(object):

    API_VERSION = 1.0

    def __init__(self, api_key):
        self._base_url = 'http://api.rottentomatoes.com/api/public/v{}'.format(API.API_VERSION)
        self.API_KEY = api_key
        self.payload = {"apikey":self.API_KEY}

    def _GET(self, url, payload=dict()):
        for k in self.payload:
            payload[k] = self.payload[k]
        # print("url: {}".format(url))
        # print("payload: {}".format(payload))
        response = requests.get(url, payload)
        response.encoding = 'utf-8'
        return response.json()

    def _build_payload(self, extra_stuff):
        payload = self.payload
        for es in extra_stuff:
            payload[es] = extra_stuff[es]
        return payload

    def _retrieve_rt_json(self, json_url):
        """
        Retrieves json at url

        returns a json dict
        >>> API = RT()
        >>> API.retrieve_rt_json("https://api.rottentomatoes.com/api/public/v1.0/movies/9385/cast.json")
        """
        valid_url = json_url.replace("https", "http")
        #print(valid_url)
        return self._GET(valid_url)

class RT(object):

    def __init__(self, api_key=API_KEY):
        self.API_KEY = api_key
        from .movies import MoviesAPI
        self.movies = MoviesAPI(self.API_KEY)

    def retrieve_rt_json(self, json_url):
        return self.movies._retrieve_rt_json(json_url)
