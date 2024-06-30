# -*- coding: utf-8 -*-

import inc
import requests
from datetime import datetime

class Bot:
    def __init__(self):
        self.db = inc.db_class.Database()
        self.mastodon = inc.mastodon_class.Mastodon()
        self.graph = inc.graph_class.Graph()
        self.json_stats = {}
        self.json_stats_checked = {}

    def getStats(self):
        """Retrieve and store Mastodon Stats"""
        stats_url = "https://api.fedidb.org/v1/stats"
        response = requests.get(stats_url)

        if response.status_code == 200:
            self.json_stats = response.json()
            return True

        else:
            if inc.cfg.debug:
                print("Failed to retrieve Mastodon statistics JSON. Response code:", response.status_code)

            return False

    def checkStats(self):
        """Checks the data collected from the Mastodon endpoint"""
        expected_data = {
            "total_users": int,
            "total_statuses": int,
            "last_updated_at": str,
            "total_instances": int,
            "total_users_str": str,
            "total_statuses_str": str,
            "total_instances_str": str,
            "monthly_active_users": int,
            "monthly_active_users_str": str
        }

        # Checks that all fields are in the collected and that the type is correct
        for field, value_type in expected_data.items():
            if field not in self.json_stats:
                print(f"Falta el campo: {field}")
                return {}

            if not isinstance(self.json_stats[field], value_type):
                print(f"Tipo incorrecto para el campo: {field}. Esperado: {value_type}, Encontrado: {type(self.json_stats[value_type])}")
                return {}

        # Validates the date format.
        try:
            datetime.fromisoformat(self.json_stats["last_updated_at"].replace("Z", "+00:00"))
        except ValueError:
            print("Formato de fecha incorrecto para el campo: last_updated_at")
            return {}

        self.json_stats_checked = self.json_stats

        return self.json_stats_checked

    def insertStats(self):
        """Insert in database the new entry"""
        json = self.checkStats()
        query = "INSERT INTO stats (total_users, total_statuses, last_updated_at, total_instances, monthly_active_users) VALUES (%d, %d, '%s', %d, %d)" % (json["total_users"], json["total_statuses"], json["last_updated_at"], json["total_instances"], json["monthly_active_users"])
        result = self.db.insert(query)

        return result

    def getStoredStats(self, last=False):
        """ Select inserted records """
        limit = 1 if last else 10

        query = "SELECT * FROM stats ORDER BY id DESC LIMIT %d" % (limit)
        result = self.db.select(query)

        return result

    def publicToot(self):
        self.graph.createGraph()
        print("🐘 Publish toot...")


    def execute(self):
        if self.getStats():
            self.checkStats()

            last_stats = self.getStoredStats(True)

            if last_stats[0]['last_updated_at'] < self.json_stats_checked['last_updated_at']:
                self.insertStats()
                self.publicToot()

        print("🏃🏻‍♂️‍➡️ Executing bot...")
