import logging
import io
import json
import urllib.request
import urllib.parse

USER_AGENT = 'Mozilla/5.0 (pls no 403erino)'

log = logging.getLogger(__name__)

def get_json(url, query_params=None, encoding='utf8'):
    if query_params:
        qs = urllib.parse.urlencode(query_params)
        url = '{0}?{1}'.format(url, qs)
    resp = urllib.request.urlopen(url)
    return json.load(io.TextIOWrapper(resp, encoding))

def get(url, query_params=None, user_agent=USER_AGENT):
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
    return urllib.request.urlopen(req)
