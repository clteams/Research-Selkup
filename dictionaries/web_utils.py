#!/usr/bin/python
# -*- coding: utf-8 -*
import urllib.request
import urllib
import time

SLEEP_SEC = 1

__author__ = "gisly"

def get_url_data(url,encoding, param_dict):
    try:
        if param_dict:
            encoded_params = urllib.parse.urlencode(param_dict)
            url = url + '?%s' % encoded_params
        urlEncoded = url
        #TODO

        time.sleep(SLEEP_SEC)
        with urllib.request.urlopen(urlEncoded) as url_socket:
            data = url_socket.read()
        return data.decode(encoding)
    except Exception as e:
        print(e)
        return None



