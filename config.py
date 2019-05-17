from pymongo import MongoClient

DATABASE = MongoClient()['restfulapi']  # DB_NAME
DEBUG = True
client = MongoClient('192.168.8.102', 37017)
