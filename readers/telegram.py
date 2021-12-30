import json
import datetime as dt

DEFAULT_PATH = "./telegram.json"

def count_messages_json(msgs,
                        chats,
                        sender=None,
                        attachs=True,
                        multattachs=False):
    for message in chats["messages"]:
        if "from" not in message or (sender is not None
                                     and message["from"] not in sender):
            continue

        date = dt.datetime.strptime(message["date"], "%Y-%m-%dT%H:%M:%S")

        if "text" in message:
            msgs.append(date)

        if not attachs:
            continue

        # attachments sent one by one in Telegram ?
        if "file" in message:
            msgs.append(date)

def count_messages(account,
                   msgs,
                   path=DEFAULT_PATH,
                   sender=None,
                   attachs=True,
                   multattachs=False):
    """Adds the times of messages to msgs.

    Arguments:
    account: the name of the chat for which we want to count the messages.
    msgs: the list containing the times of each messages.
    path: the path to the json file containing the conversations. Defaults to  DEFAULT_PATH.
    sender: either a string corresponding to the name of a sender, a set of senders, or None. If None, all senders are counted.
    attachs: a boolean indicating whether attachments (files, gifs, stickers, images, videos, etc) are counted as messages. Defaults to True.
    multattachs: a boolean indicating whether multiple attachments sent at once are counted several messages.
    Default to False. Doesn't matter if `attachs` is False.
    """

    with open(path, encoding='utf8') as reader:
        allmsgs = json.load(reader)

        if isinstance(sender, str):
            sender = {sender}

        for chats in allmsgs["chats"]["list"]:
            if chats["name"] == account:
                count_messages_json(msgs, chats, sender, attachs, multattachs)

def count_all_messages(msgs,
                       sender=None,
                       path=DEFAULT_PATH,
                       attachs=True,
                       multattachs=False):
    with open(path, encoding='utf8') as reader:
        allmsgs = json.load(reader)

        if isinstance(sender, str):
            sender = {sender}

        for chats in allmsgs["chats"]["list"]:
            count_messages_json(msgs, chats, sender, attachs, multattachs)

# Initiate Telegram command line parameters
def init(parser):
    group = parser.add_argument_group("telegram", "Telegram options")

    # Telegram parameters
    group.add_argument(
        '--tgaccount',
        type=str,
        action="store",
        help=
        "the name of the chat we want to count messages from. Has to be specified to count Telegram messages"
    )
    group.add_argument(
        '--tgpath',
        type=str,
        action="store",
        default=DEFAULT_PATH,
        help=
        f"the path to the json file generated by Telegram. Defaults to \"{DEFAULT_PATH}\""
    )
    group.add_argument(
        '--tgsender',
        type=str,
        action='append',
        default=None,
        help=
        "the list of considered senders. If not specified, all messages are counted. Use once per sender"
    )

def parse(msgs, values):
    if values["all"]:
        if values["tgsender"] is not None:
            count_all_messages(msgs,
                               values["tgsender"],
                               path=values["tgpath"],
                               attachs=not values["no_attachs"],
                               multattachs=values["multi_attachs"])
    elif values["tgaccount"] is not None:
        count_messages(values["tgaccount"],
                       msgs,
                       sender=values["tgsender"],
                       path=values["tgpath"],
                       attachs=not values["no_attachs"],
                       multattachs=values["multi_attachs"])
