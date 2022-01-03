from userbot.database import Chat as DbChat, User as DbUser
from pyrogram.types import Chat, User, Message
from uuid import uuid4
from os import rename
from pathlib import Path


def insert_chat(chat: Chat):
    if chat_obj := DbChat.get(id=chat.id):
        return chat_obj
    return DbChat(
        id=chat.id,
        type=chat.type,
        username=chat.username,
        title=chat.first_name or chat.title
    )


def insert_user(user: User):
    if user_obj := DbUser.get(id=user.id):
        return user_obj
    return DbUser(
        id=user.id,
        first_name=user.first_name,
        username=user.username,
        is_bot=user.is_bot,
        profile_picture=getattr(user.photo, "big_file_id", None)
    )


def get_media(message: Message):
    return (
            message.photo
            or message.document
            or message.audio
            or message.animation
            or message.sticker
            or message.video
            or message.video_note
            or message.voice
    )


def modify_path(path: str):
    if path:
        path = Path(path)
        new_name = uuid4().hex + "." + path.name.rsplit(".")[-1]
        rename(str(path), str(path.parent / new_name))
        return str(path.parent / new_name)
    return uuid4().hex

