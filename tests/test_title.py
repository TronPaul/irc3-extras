from irc3.testing import BotTestCase
from irc3_extras.title import handler


@handler(r'testurl.com.*')
def handler1(url):
    return 'Done'

@handler(r'dicttest.com.*')
def handler2(url):
    return {'This': 'test'}


class TestTitle(BotTestCase):
    name = 'irc3_extras.title'

    config = dict(includes=[name])

    def test_url(self):
        bot = self.callFTU(nick='foo')
        bot.dispatch(':bar!user@host PRIVMSG #chan :http://google.com')
        self.assertSent(['PRIVMSG #chan :\x02google.com:\x02 Google'])

    def test_handler(self):
        bot = self.callFTU(nick='foo')
        bot.include(__name__)
        bot.dispatch(':bar!user@host PRIVMSG #chan :http://testurl.com/a/b/c')
        self.assertSent(['PRIVMSG #chan :Done'])

    def test_dict_formatter(self):
        bot = self.callFTU(nick='foo')
        bot.include(__name__)
        bot.dispatch(':bar!user@host PRIVMSG #chan :http://dicttest.com/a/b/c')
        self.assertSent(['PRIVMSG #chan :\x02This:\x02 test'])