# -*- coding: utf-8 -*-

import inc

def main():
    # Checking the internet connection.
    if inc.cm.check_internet() is True:
        mastodon_community_manager_bot = inc.cm_class.MastodonCM()
        mastodon_community_manager_bot.execute()

if __name__ == "__main__":
    main()
