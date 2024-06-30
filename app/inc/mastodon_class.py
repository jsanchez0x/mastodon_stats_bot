# -*- coding: utf-8 -*-

import os
from mastodon import Mastodon as MastodonPy
import imghdr
import inc
from PIL import Image
from pprint import pprint

class Mastodon:

    def __init__(self, post_visibility = 'unlisted'):
        self.__api = self.__create_api()
        self.__app = None

        self.post_visibility = post_visibility

    def __create_api(self):
        api = MastodonPy(
            access_token = inc.cfg.mastodon["access_token"],
            api_base_url = 'https://masto.es',
            user_agent = 'TecladosTrackerBot'
        )

        return api


    ######################
    # CONNECTION METHODS #
    ######################

    def check_connection(self):
        try:
            me = self.__app

            if me.vapid_key is not None:
                if inc.cfg.debug:
                    print("Connection is established with Mastodon.")

                return True
            else:
                if inc.cfg.debug:
                    print("Mastodon connection is closed or connected user info can not be retrieve.")

                return False
        except AttributeError:
            if inc.cfg.debug:
                inc.cm.print_error("Mastodon class was initialized without login.")

            return False

    def connect(self):
        if inc.cfg.debug:
            print("Trying to verify APP credentials...")

        try:
            app_information = self.__api.app_verify_credentials()
            self.__app = app_information

            if inc.cfg.debug:
                print("Logged into Mastodon. Getting logged app info...")
                pprint(app_information, indent=2)
        except Exception as e:
            inc.cm.print_error(str(e))


    ###################
    # POSTING METHODS #
    ###################

    def post_image(self, url, message, temp_img, temp_img_thumb, thumb_sizes):
        downloaded = inc.cm.download_file(url, temp_img)

        if downloaded:
            # If image is larger than 4883kb, resize and fix None type in image
            if os.path.getsize(temp_img) > inc.cfg.mastodon["max_image_filesize"] or imghdr.what(temp_img) is None:
                im = Image.open(temp_img)

                # Convert to RGB
                if im.mode != 'RGB':
                    im = im.convert('RGB')

                im.thumbnail(thumb_sizes)
                im.save(temp_img_thumb, "JPEG", quality=90)

                media_upload = self.upload_image(temp_img_thumb)
                os.remove(temp_img_thumb)
            else:
                media_upload = self.upload_image(temp_img)

            os.remove(temp_img)

            if inc.cfg.debug:
                print("Tooting with image: " + message)

            if inc.cfg.mastodon_interaction and hasattr(media_upload, 'id') :
                try:
                    self.__api.status_post(message, media_ids = media_upload, visibility = self.post_visibility)
                except Exception as e:
                    inc.cm.print_error("Error posting an update with image on Mastodon. " + str(e))

    def upload_image(self, path):
        if inc.cfg.debug:
            print("Upload image to Mastodon: " + path)

        if inc.cfg.mastodon_interaction:
            return self.__api.media_post(path)
        else:
            return ''

    def post_text(self, message):
        if inc.cfg.debug:
            print("Tooting only text: " + message)

        if inc.cfg.mastodon_interaction:
            self.__api.status_post(message, visibility = self.post_visibility)


    #################
    # LISTS METHODS #
    #################

    def get_list_from_name(self, name):
        lists = self.__api.lists()
        list = None

        for list in lists:
            if list.title == name:
                list = self.__api.list(list.id)

        return list

    def get_list_from_id(self, id):
        return self.__api.list(id)

    def get_list_members(self, list_id):
        return self.__api.list_accounts(list_id)

    def add_list_member(self, list_id, member_id):
        if inc.cfg.debug:
            user = self.get_user_from_id(member_id)
            list = self.get_list_from_id(list_id)
            print("Add Mastodon member %s to list %s" % (user.acct, list.title))

        if inc.cfg.mastodon_interaction:
            self.__api.list_accounts_add(list_id, member_id)

    def remove_list_member(self, list_id, member_id):
        if inc.cfg.debug:
            user = self.get_user_from_id(member_id)
            list = self.get_list_from_id(list_id)
            print("Remove Mastodon member %s to list %s" % (user.acct, list.title))

        if inc.cfg.mastodon_interaction:
            self.__api.list_accounts_delete(list_id, member_id)


    ###################
    # FRIENDS METHODS #
    ###################

    def follow(self, user_id):
        if inc.cfg.debug:
            user = self.get_user_from_id(user_id)
            print("Follow Mastodon user %s" %  user.acct)

        if inc.cfg.mastodon_interaction:
            self.__api.account_follow(user_id)

    def unfollow(self, user_id):
        if inc.cfg.debug:
            user = self.get_user_from_id(user_id)
            print("Unfollow Mastodon user %s" %  user.acct)

        if inc.cfg.mastodon_interaction:
            self.__api.account_unfollow(user_id)

    def get_my_follows(self):
        me = self.__api.me()
        followings = self.__api.account_following(me.id)
        followings_ids = []

        for user in followings:
            followings_ids.append(user.id)

        return followings_ids

    def get_followers(self):
        me = self.__api.me()
        followers = self.__api.account_followers(me.id)
        followers_ids = []

        for user in followers:
            followers_ids.append(user.id)

        return followers_ids


    #################
    # USERS METHODS #
    #################

    def get_user_from_id(self, id):
        return self.__api.account(id)