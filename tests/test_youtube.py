from irc3.testing import BotTestCase
from unittest import mock

MagicMock = mock.MagicMock
patch = mock.patch


class TestTitle(BotTestCase):
    name = 'irc3_extras.youtube'

    config = {
        'includes': [name],
        'irc3_extras.youtube': {
            'api_key': 'fake_key'
        }}

    def patch_get_json(self, json=None):
        patcher = patch('irc3_extras.http.get_json')
        self.addCleanup(patcher.stop)
        get_json = patcher.start()
        json = json or {}
        get_json.return_value = json
        return get_json

    def test_handler(self):
        self.patch_get_json({'items': [{'snippet': {
            'title': 'A',
            'channelTitle': 'B'
        }, 'statistics': {
            'viewCount': 9001,
            'likeCount': 0,
            'dislikeCount': 10
        }, 'contentDetails': {
            'duration': 'PT14S',
        }}]})
        bot = self.callFTU(nick='foo')
        bot.dispatch(':bar!user@host PRIVMSG #chan :http://www.youtube.com/watch?v=1VCwSCRNcps')
        self.assertSent(['PRIVMSG #chan :\x02Title:\x02 A \x02By:\x02 B \x02Views:\x02 9001 \x02Duration:\x02 PT14S \x02Likes:\x02 0 \x02Dislikes:\x02 10'])