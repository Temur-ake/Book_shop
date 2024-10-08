import os
from os import getenv
from dotenv import load_dotenv
from redis_dict import RedisDict
load_dotenv()
TOKEN = os.getenv("TOKEN")

ADMIN_LIST = [6067978806,]
database = RedisDict('books')
