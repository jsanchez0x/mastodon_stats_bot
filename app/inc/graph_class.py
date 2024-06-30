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

    def createGraph(self):
        url = 'https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/gapminderData.csv'
        df = pd.read_csv(url)

        # Subset rows for France only
        df = df[df['country']=='France']

        # Create and display the linechart
        df.plot(x='year',
                       y='lifeExp',
                       kind='line', # (facultative) Default argument
                       grid=True, # Add a grid in the background
                      )

        plt.savefig('grafico.png')