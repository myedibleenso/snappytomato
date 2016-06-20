#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def normalize_text(text):
    return text.lower()

def attach_attributes(obj, data_dict):
    for d in data_dict:
        setattr(obj, d, data_dict[d])

def load_api_key(rtkey):
    """
    Loads api key from provided path

    >>> load_api_key("~/path/to/my/rt/key")
    returns api key
    """
    with open(os.path.expanduser(rtkey), 'r') as kf:
        key = kf.read().strip()
    return key
