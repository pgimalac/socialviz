import json
import datetime as dt

# Returns the number of messages for each date, for the given json messages.
def count_messages_json(msgs,
                        counter,
                        sender=None,
                        attachs=True,
                        multattachs=False):
    attachtypes = ["photos", "gifs", "files"]

    if isinstance(sender, str):
        sender = {sender}

    for message in msgs["messages"]:
        if message["is_unsent"]:
            continue

        if sender is not None and message["sender_name"] not in sender:
            continue

        date = dt.datetime.fromtimestamp(message["timestamp_ms"] //
                                         1000).date()

        if "content" in message:
            counter[date] = counter.get(date, 0) + 1

        if not attachs:
            continue

        nbattachs = sum([
            len(message[attach]) for attach in attachtypes if attach in message
        ])
        if multattachs:
            counter[date] = counter.get(date, 0) + nbattachs
        elif nbattachs > 0:
            counter[date] = counter.get(date, 0) + 1

def count_messages(account,
                   counter,
                   path="./messages/inbox/",
                   sender=None,
                   attachs=True,
                   multattachs=False):
    """Adds the number of messages for each date to the counter.

    Arguments:
    account: the name of the directory corresponding to the wanted account.
    counter: the dictionary containing the number of messages for each date.
    path: the actual path to the inbox directory. Defaults to  "./messages/inbox".
    sender: either a string corresponding to the name of a sender, a set of senders, or None. If None, all senders are counted.
    attachs: a boolean indicating whether attachments (files, gifs, stickers, images, videos, etc) are counted as messages. Defaults to True.
    multattachs: a boolean indicating whether multiple attachments sent at once are counted several messages.
    Default to False. Doesn't matter if `attachs` is False.
    """

    number = 0
    while True:
        number += 1
        try:
            with open(path + account + f"/message_{number}.json",
                      encoding='utf8') as reader:
                msgs = json.load(reader)
                count_messages_json(msgs, counter, sender, attachs,
                                    multattachs)
        except FileNotFoundError:
            return
