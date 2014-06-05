import json
import re
import io
import irc3
import logging
from urllib.parse import urlparse
from irc3_extras import title
from irc3_extras import http

API_URL = 'https://www.googleapis.com/youtube/v3/videos'
DURATION_RE = re.compile(r'^PT((?P<minutes>[0-9]+)M)?((?P<seconds>[0-9]+)S)?$')

@irc3.plugin
class YoutubeHandler:
    requires = [
        'irc3_extras.title'
    ]

    def __init__(self, bot):
        self.config = config = bot.config.get(__name__, {})
        self.api_key = self.config.get('api_key', None)
        self.log = logging.getLogger(__name__)

    @title.handler(r'(youtu\.be/.+|(www\.)?youtube\.com/.+[?&]v=.*)')
    def youtube(self, url):
        assert self.api_key
        o = urlparse(url)
        if re.search(r'youtub\.be', o.netloc):
            vid = o.path[1:-1].split('&')[0]
        else:
            q = [qp for qp in o.query.split('&') if qp[:2] == 'v='][0]
            vid = q.split('=')[1]

        opts = {
            'id': vid,
            'part': 'contentDetails,statistics,snippet',
            'key': self.api_key
        }

        self.log.debug('Youtube %r', vid)
        d = http.get_json(API_URL, opts)['items'][0]
        return {
            'Title': d['snippet']['title'],
            'By': d['snippet']['channelTitle'],
            'Views': d['statistics']['viewCount'],
            'Duration': d['contentDetails']['duration'],
            'Likes': d['statistics']['likeCount'],
            'Dislikes': d['statistics']['dislikeCount']
        }
