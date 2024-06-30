# -*- coding: utf-8 -*-

import os

# Configuration
base_folder = os.getenv('APP_HOME') + "/"
data_folder = base_folder + "data/volume/"
debug = True if 'APP_DEBUG' in os.environ else False
db_changes = True if 'APP_DB_CHANGES' in os.environ else False

mastodon_interaction = True if 'APP_MASTODON_INTERACTION' in os.environ else False
mastodon_image_max_thumb_sizes = 1500, 1500

mastodon = {
              "access_token": os.getenv('APP_MASTODON_ACCESS_TOKEN'),
       "max_image_filesize": 4883000,
           "max_characters": 1000
}
