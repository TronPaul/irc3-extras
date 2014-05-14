from irc3 import utils
import functools
import venusian
import fnmatch
import logging
import docopt
import irc3
import sys
import re

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
    return {domain: page.title.text}

class handler(object):
    venusian = venusian

    def __init__(self, regex, *func):
        self.regex = regex
        self.cregex = re.compile(regex)
        if func:
            self.__call__ = self.func = func[0]
            self.info = self.venusian.attach(self, self.callback,
                                             category=self.__module__)
        self.category = self.__module__

    def callback(self, context, name, ob):
        bot = context.bot
        if self.info.scope == 'class':
            callback = self.func.__get__(bot.get_plugin(ob), ob)
        else:
            @functools.wraps(self.func)
            def wrapper(*args, **kwargs):
                return self.func(*args, **kwargs)
            callback = wrapper
        plugin = bot.get_plugin(UrlHandlers)
        plugin.handlers.append((self.regex, callback))
        bot.log.info('Register url %r', self.func.__name__)

    def __call__(self, func):
        self.__call__ = self.func = func
        self.info = self.venusian.attach(func, self.callback,
                                         category=self.category)
        return func


@irc3.plugin
class UrlHandlers:

    requires = [
        'irc3.plugins.core',
    ]

    def __init__(self, bot):
        self.bot = bot
        self.config = config = bot.config.get(__name__, {})
        self.log = logging.getLogger(__name__)
        self.log.debug('Config: %r', config)
        self.handlers = []

    def get_handler(self, url):
        for cregex, h in self.handlers:
            if cregex.find(url):
                return h
        else:
            return default_handler

    @irc3.event(irc3.rfc.PRIVMSG)
    def on_message(self, mask=None, event=None, target=None, data=None):
        self.log.debug('Handlers: %r', self.handlers)
        if target.is_channel and event == 'PRIVMSG':
            urls = URL_REGEX.findall(data)
            for url in urls:
                f = self.get_handler(url)
                if f is not None:
                    try:
                        msg = f(url)
                    except Exception:
                        self.log.exception('Error building message from url')
                        msg = None
                    if msg:
                        msg = format_message(msg)
                        self.bot.privmsg(target, msg)

    def __repr__(self):
        return '<UrlHandlers %s>' % sorted([r for r, _ in self.handlers])
