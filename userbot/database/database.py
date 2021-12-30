from configparser import ConfigParser
from pony.orm import Database


config = ConfigParser()
config.read("config.ini")

db = Database("postgres", **config["database"])
