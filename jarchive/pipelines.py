# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class JarchivePipeline(object):
    def process_item(self, item, spider):
        return item


class JarchiveSQLPipeline(object):
    filename = 'jarchive.sqlite'
    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)
        return

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_tables()
        return

    def create_tables(self):
        conn = sqlite3.connect(self.filename)
        conn.execute('PRAGMA foreign_keys=ON')
        conn.execute('CREATE TABLE games (key integer primary key autoincrement, title text, number text, url text, id text)')
        conn.execute('CREATE TABLE questions (key integer primary key autoincrement, game_key integer, id text, text text, answer text, value text, url_id text, type text, cat text, jround text, foreign key(game_key) references games(key))')
        conn.commit()
        return conn
        
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None        
        return

    def process_item(self, item, spider):
        self.conn.execute('insert into games(title, number, url, id) values (?,?,?,?)', 
                          (str(item['game_title']),
                           item['game_number'],
                           item['game_url'],
                           item['game_id'])
        )
        game_row = self.conn.cursor().lastrowid
        
        for q in item['questions']:
            self.conn.execute('INSERT INTO questions(id, text, answer, value, url_id, type, cat, jround, game_key) VALUES (?,?,?,?,?,?,?,?,?)', 
                              (q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], game_row)
        )
        return item
