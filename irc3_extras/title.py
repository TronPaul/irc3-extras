import re
import urllib.request as request
import irc3
import bs4

URL_REGEX = re.compile(r'https?://\S+')
DOMAIN_REGEX = re.compile(r'https?://(?P<domain>[^/]+)(/\S+)?')

def format_message(o):
    if isinstance(o, dict):
        parts = ['\02{key}:\02 {value}'.format(key=k, value=format_message(v)) for k, v in o.items()]
        return ' '.join(parts)
    else:
        return o

def default_handler(url):
    resp = request.urlopen(url)
    page = bs4.BeautifulSoup(resp)
    m = re.match(DOMAIN_REGEX, url)
    if m:
        domain = m.group('domain')
    else:
        domain = url[:10]
    return {domain:page.title.text}

@irc3.plugin
class TitlePlugin:
    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.PRIVMSG)
    def on_message(self, mask=None, event=None, target=None, data=None):
        if event == 'PRIVMSG' and target.is_channel:
             urls = URL_REGEX.findall(data)
             for url in urls:
                 self.on_url(target, url)

    def on_url(self, dest, url):
        msg = default_handler(url)
        msg = format_message(msg)
        print(msg)
        self.bot.privmsg(dest, msg)
