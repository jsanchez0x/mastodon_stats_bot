# -*- coding: utf-8 -*-

import inc
import sqlite3

class Database:
    def __init__(self):
        self.__connection = None

        try:
            db_path = inc.cfg.data_folder + 'db.sqlite'
            self.__connection = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print("Database error %s" % (e))

        self.__connection.row_factory = sqlite3.Row
        self.__cursor = self.__connection.cursor()

    def select(self, query):
        if inc.cfg.debug:
            print("DB select: %s" % query)

        self.__cursor.execute(query)
        result = self.__cursor.fetchall()

        if inc.cfg.debug:
            self.debug_select_result(result)

        return result

    def insert(self, query):
        if inc.cfg.debug:
            print("DB insert: %s" % query)

        if inc.cfg.db_changes:
            self.__cursor.execute(query)
            self.__connection.commit()
            result = self.__cursor.lastrowid

            if inc.cfg.debug:
                print("  Insert id: %s" % result)

            return result
        else:
            if inc.cfg.debug:
                print("  Result: database changes flag disabled")

            return 0

    def update(self, query):
        if inc.cfg.debug:
            print("DB update: %s" % query)

        if inc.cfg.db_changes:
            self.__cursor.execute(query)
            self.__connection.commit()

    def delete (self, query):
        if inc.cfg.debug:
            print("DB delete: %s" % query)

        if inc.cfg.db_changes:
            self.__cursor.execute(query)
            self.__connection.commit()

    def debug_select_result(self, result):
        string_result = ''
        for row in result:
            for key in row.keys():
                string_result = string_result + "[" + key + ': ' + str(row[key]) + '], '

        print(" Result: %s" % string_result)