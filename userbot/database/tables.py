from userbot.database import db
from pony.orm import PrimaryKey, Required, Optional, Set
from datetime import datetime


class User(db.Entity):
    id = PrimaryKey(int, size=64)
    first_name = Required(str)
    username = Optional(str, nullable=True)
    is_bot = Required(bool)
    profile_picture = Optional(str, nullable=True)
    messages = Set("MessageFrame")


class Chat(db.Entity):
    id = PrimaryKey(int, size=64)
    type = Required(str)
    username = Optional(str, nullable=True)
    title = Required(str)
    messages = Set("MessageFrame")


class MessageFrame(db.Entity):
    id = PrimaryKey(int, auto=True)
    message_id = Required(int, size=64)
    sender = Required(User)
    chat = Required(Chat)
    date = Required(datetime)
    versions = Set("MessageVersion")


class Media(db.Entity):
    id = PrimaryKey(int, auto=True)
    type = Required(str)
    width = Optional(int, size=32, nullable=True)
    height = Optional(int, size=32, nullable=True)
    path = Optional(str, nullable=True)
    file_size = Required(int, size=32)
    file_name = Optional(str, nullable=True)
    mime_type = Optional(str, nullable=True)
    duration = Optional(int, size=32, nullable=True)
    frame = Optional("MediaFrame")


class MediaFrame(db.Entity):
    id = PrimaryKey(int, auto=True)
    media_group = Required(bool)
    media_group_id = Optional(int, size=64, nullable=True)
    media = Set(Media)
    version = Optional("MessageVersion")


class MessageVersion(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Optional(str, nullable=True)
    date = Required(datetime)
    media = Optional(MediaFrame, nullable=True)
    message_frame = Optional("MessageFrame")


db.generate_mapping(create_tables=True)
