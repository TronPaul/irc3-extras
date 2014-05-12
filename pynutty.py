import irc3

def main():
    irc3.IrcBot(
        nick='irc3-tron', autojoins=['#tron.test.irc3'],
        host='NuclearFallout.WA.US.GameSurge.net', port=6667, ssl=False, verbose =True,
        includes=[
            'irc3.plugins.core',
            'irc3_extras.title',
        ]).run()
 
if __name__ == '__main__':
    main()
