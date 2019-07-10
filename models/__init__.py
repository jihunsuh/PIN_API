from peewee import SqliteDatabase
import sqlite3

connection = sqlite3.connect('test_sqlite.db')
curser = connection.cursor()

DB = SqliteDatabase('test_peewee.db')
