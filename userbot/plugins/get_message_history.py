from pyrogram import filters, types, Client
from userbot.html_gen.generator import generate_edit_history
from pony.orm import db_session
from userbot.database.tables import MessageFrame
from userbot.utilities import insert_chat
from io import BytesIO


@Client.on_message(filters.command("eh", "!") & filters.user("jonatan1609"), group=1)
def get_message_history(_, message: types.Message):
    if not message.reply_to_message:
        return message.reply("You have to reply to a message!")
    with db_session:
        chat = insert_chat(message.chat)
        frame = MessageFrame.get(chat=chat, message_id=message.reply_to_message.message_id)
        if not frame:
            return message.reply("No edits available for that message!")
        doc = BytesIO(generate_edit_history(frame).encode())
        doc.name = "edit-history.html"
        return message.reply_to_message.reply_document(doc, quote=True)
