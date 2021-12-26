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
