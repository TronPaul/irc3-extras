import json
import re
import io
import irc3
import logging
from irc3_extras import title
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen

API_URL = 'https://www.googleapis.com/youtube/v3/videos'
DURATION_RE = re.compile(r'^PT((?P<minutes>[0-9]+)M)?((?P<seconds>[0-9]+)S)?$')

@irc3.plugin
class YoutubeHandler:
    def __init__(self, bot):
        self.api_key = bot.config.get('irc3_extras.youtube.api_key', None)
        self.log = logging.getLogger(__name__)

    @title.handler('r(youtu\.be/.+|(www\.)?youtube\.com/.+[?&]v=.*)')
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

        qs = urlencode(opts)
        api_url = '{api}?{qs}'.format(api=API_URL, qs=qs)
        self.log.debug('Youtube %r', api_url)
        resp = urlopen(api_url)
        d = json.load(io.TextIOWrapper(resp))['items'][0]
        return {
            'YouTube': d['snippet']['title'],
            'By': d['snippet']['channelTitle'],
            'Views': d['statistics']['viewCount'],
            'Duration': d['contentDetails']['duration'],
            'Likes': d['statistics']['likeCount'],
            'Dislikes': d['statistics']['dislikeCount']
        }
