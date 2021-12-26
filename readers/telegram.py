import json
import datetime as dt

def count_messages(account,
                   counter,
                   path="./telegram.json",
                   sender=None,
                   attachs=True,
                   multattachs=False):
    """Adds the number of messages for each date to the counter.

    Arguments:
    account: the name of the chat for which we want to count the messages.
    counter: the dictionary containing the number of messages for each date.
    path: the path to the json file containing the conversations. Defaults to  "./telegram.json".
    sender: either a string corresponding to the name of a sender, a set of senders, or None. If None, all senders are counted.
    attachs: a boolean indicating whether attachments (files, gifs, stickers, images, videos, etc) are counted as messages. Defaults to True.
    multattachs: a boolean indicating whether multiple attachments sent at once are counted several messages.
    Default to False. Doesn't matter if `attachs` is False.
    """

    with open(path, encoding='utf8') as reader:
        msgs = json.load(reader)

        if isinstance(sender, str):
            sender = {sender}

        for chats in msgs["chats"]["list"]:
            if chats["name"] == account:
                for message in chats["messages"]:
                    if sender is not None and message["from"] not in sender:
                        continue

                    date = dt.datetime.strptime(message["date"],
                                                "%Y-%m-%dT%H:%M:%S").date()

                    if "text" in message:
                        counter[date] = counter.get(date, 0) + 1

                    if not attachs:
                        continue

                    # attachments sent one by one in Telegram ?
                    if "file" in message:
                        counter[date] = counter.get(date, 0) + 1

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
        default="./telegram.json",
        help=
        "the path to the json file generated by Telegram. Defaults to \"./telegram.json\""
    )
    group.add_argument(
        '--tgsender',
        type=str,
        action='append',
        default=None,
        help=
        "the list of considered senders. If not specified, all messages are counted. Use once per sender"
    )

def parse(counter, values):
    if values["tgaccount"] is not None:
        count_messages(values["tgaccount"],
                       counter,
                       sender=values["tgsender"],
                       path=values["tgpath"],
                       attachs=not values["no_attachs"],
                       multattachs=values["multi_attachs"])
