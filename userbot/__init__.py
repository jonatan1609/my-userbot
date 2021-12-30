from pyrogram import Client
from .database import *

max_media_size = config.getint("userbot", "max_media_size")
app = Client("UserBot")
