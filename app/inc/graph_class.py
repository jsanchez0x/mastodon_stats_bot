# -*- coding: utf-8 -*-

import inc
import pandas as pd
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.db = inc.db_class.Database()
        self.mastodon = inc.mastodon_class.Mastodon()
        self.json_stats = {}
        self.json_stats_checked = {}