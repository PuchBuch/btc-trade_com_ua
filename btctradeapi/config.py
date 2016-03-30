from threading import Thread
from peewee import SqliteDatabase

"""
THREAD PARENT
"""
THREAD_PARENT = Thread

DB = SqliteDatabase(":memory:")
