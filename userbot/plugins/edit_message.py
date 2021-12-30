import datetime
from pyrogram import Client, types
from userbot.database import MessageFrame, MessageVersion, MediaFrame, Media
from userbot.utilities import insert_chat, insert_user, get_media, modify_path
from pony.orm import db_session
from userbot import max_media_size

# todo: fix media group


@Client.on_message()
async def edit_message_handler(client: Client, message: types.Message):
    if not message.from_user:
        return
    media = None
    if message.media and not message.media_group_id:
        media = get_media(message)
        if media:
            media = MediaFrame(
                media_group=False,
                media_group_id=None,
                media=[
                    Media(
                        type=media.__class__.__name__,
                        width=getattr(media, "width", None),
                        height=getattr(media, "height", None),
                        path=modify_path(await client.download_media(message))
                        if media.file_size <= max_media_size else media.file_id,
                        file_size=media.file_size,
                        file_name=getattr(media, "file_name", None),
                        mime_type=getattr(media, "mime_type", None),
                        duration=getattr(media, "duration", None),
                    )
                ]
            )
    version = MessageVersion(
        text=message.text or message.caption,
        date=datetime.datetime.fromtimestamp(message.edit_date or message.date),
        media=media
    )
    with db_session:
        chat = insert_chat(message.chat)
        user = insert_user(message.from_user)
        if not MessageFrame.get(chat=chat, message_id=message.message_id):
            MessageFrame(
                message_id=message.message_id,
                sender=user,
                chat=chat,
                date=datetime.datetime.fromtimestamp(message.date),
                versions=[version]
            )
        else:
            MessageFrame.get(chat=chat, message_id=message.message_id).versions.add(version)
