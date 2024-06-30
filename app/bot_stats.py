# -*- coding: utf-8 -*-

import inc

def main():
    # Checking the internet connection.
    if inc.cm.check_internet() is True:
        mastodon_stats_bot = inc.bot_class.Bot()
        mastodon_stats_bot.execute()

if __name__ == "__main__":
    main()
