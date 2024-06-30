# -*- coding: utf-8 -*-

import inc
import time

class CommunityManager:
    def do_unfollows(self, users, followers_ids, follows_ids, list_id):
        for member in users:

            if member.id not in followers_ids: # Not follower, remove from list.
                self.social_network.remove_list_member(list_id, member.id)

                if member.id in follows_ids: # Its follow by me, unfollow.
                    self.social_network.unfollow(member.id)

    def do_follows(self, followers_ids, follows_ids, list_id):
        inc.cm.print_error("Implement method in subclass")

    def execute(self):
        list = self.social_network.get_list_from_name(inc.cfg.manage_twitter_bot["follow_back_list"])
        list_members = self.social_network.get_list_members(list.id)
        followed_by_me = self.social_network.get_my_follows()
        followers = self.social_network.get_followers()

        self.do_unfollows(list_members, followers, followed_by_me, list.id)
        self.do_follows(followers, followed_by_me, list.id)


#####################
# MASTODON SUBCLASS #
#####################

class MastodonCM(CommunityManager):
    def __init__(self):
        self.social_network = inc.mastodon_class.Mastodon()

    def do_follows(self, followers_ids, follows_ids, list_id):
        for follower_id in followers_ids:

            if follower_id not in follows_ids: # It is a follower that I do not follow.
                try:
                    follower = self.social_network.get_user_from_id(follower_id)

                    if follower.locked is not True: # Not follow private users.
                        self.social_network.follow(follower_id)

                except Exception as e:
                    inc.cm.print_error("Error following Mastodon user %s: %s" % (follower.username, e))

            # Users can only be added to a list when they are followed.
            # The sleep is added because Mastodon takes time to register the follow.
            time.sleep(10)

            # Add to follow back list
            members = self.social_network.get_list_members(list_id)

            members_ids = []
            for member in members:
                members_ids.append(member.id)

            try:
                members_ids.index(follower_id)

            except ValueError:
                self.social_network.add_list_member(list_id, follower_id)
