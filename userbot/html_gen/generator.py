from userbot.database.tables import MessageFrame, MessageVersion
from .html import *


def generate_username(username: str):
    return ElementA(f"@{username}", href=f"https://t.me/{username}")


def generate_edit_history(message_frame: MessageFrame) -> str:
    elements = [
        ElementCenter(ElementH2(ElementU("Edit history"))),
        ElementSpan("Name: " + ElementI(message_frame.sender.first_name)),
        ElementSpan(" [" + ElementStrong(["User", "Bot"][message_frame.sender.is_bot]) + "]")
    ]
    if message_frame.sender.username:
        elements.append(ElementBr() + ElementSpan("Username: " + generate_username(message_frame.sender.username)))
    elements.append(ElementBr() + ElementSpan("Chat: " + ElementI(message_frame.chat.title)))
    if message_frame.chat.username:
        elements.append(ElementBr() + ElementSpan("Chat's Username: " + generate_username(message_frame.chat.username)))
    elements.append(ElementBr())
    elements.extend([ElementDiv(
        ElementDiv(
            ElementU(version.date) + ":" + ElementTextArea(version.text, readonly=True, style="margin-left: 7px"),
            style="display: flex;align-items:center"
        ),
        style="border: 1px black solid; display: inline-block; padding:10px; margin: 5px"
    ) + ElementBr() for version in message_frame.versions.sort_by(MessageVersion.date)])
    return "".join(Element.fetch(element) for element in elements)

