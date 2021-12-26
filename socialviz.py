import pandas as pd
from matplotlib import pyplot as plt
import json
import datetime as dt
import numpy as np
import math

# attachs: a boolean indicating whether attachments (images, files, gifs) are counted as messages.
attachs = True

# multattachs: a boolean indicating whether multiple attachments sent at once are counted as several.
multattachs = False

# Returns the number of messages for each date, for the given json messages.
def count_messages_facebook_json(msgs, counter=dict(), sender=None):
    attachtypes = ["photos", "gifs", "files"]

    if sender is None:
        sender = set([name["name"] for name in msgs["participants"]])

    if type(sender) is str:
        sender = {sender}

    for message in msgs["messages"]:
        if message["is_unsent"] or message["sender_name"] not in sender:
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
    return counter

def count_messages_facebook(account,
                            counter=dict(),
                            path="./messages/inbox/",
                            sender=None):
    """Returns the number of messages for each date.

    Arguments:
    account: the name of the directory corresponding to the wanted account.
    counter: the dictionnary containing the number of messages for each date.
    path: the actual path to the inbox directory. Defaults to  "./messages/inbox".
    sender: either a string corresponding to the name of a sender, a set of senders, or None. If None, all senders are counted.
    """

    number = 0
    while True:
        number += 1
        try:
            with open(path + account + f"/message_{number}.json") as reader:
                msgs = json.load(reader)
                count_messages_facebook_json(msgs, counter, sender)
        except FileNotFoundError:
            return counter

# Iterates from first to last inclusive, with the given step.
def iterdate(first, last, step=dt.timedelta(days=1)):
    while first <= last:
        yield first
        first += step

# Build the dataframe
def df_from_counter(counter):
    df = pd.DataFrame()
    df["time"] = counter.keys()
    df["count"] = counter.values()
    df.set_index("time", inplace=True)

    # Fill missing dates, between first and last
    alldates = pd.DataFrame(index=list(iterdate(min(df.index), max(df.index))))
    missing = pd.DataFrame(index=alldates.index.difference(df.index))
    missing["count"] = 0
    df = df.append(missing)

    # Generate helper columns
    df["year"] = df.index.to_series().apply(lambda time: time.year)
    df["month"] = df.index.to_series().apply(lambda time: time.month)
    df["year-month"] = df.index.to_series().apply(
        lambda time: f"{time.year}-{time.month:02}")
    df["day"] = df.index.to_series().apply(lambda time: time.day)
    return df

# Returns the value for the given month and day, or NaN if there is no such value.
def get_value(day, month):
    try:
        return df[(df["year-month"] == month)
                  & (df["day"] == day)]["count"].iloc[0]
    except IndexError:
        return float("nan")

def display_values_per_day(df):
    months = sorted(reversed(df["year-month"].drop_duplicates()))
    days = list(range(1, 32))
    counts = [[get_value(day, month) for month in months] for day in days]

    counts = np.array(counts)

    plt.figure(figsize=(20, 10))
    plt.imshow([[math.log(1 + x) for x in y] for y in counts],
               interpolation='none',
               aspect="auto",
               vmax=6.5)

    for (j, i), label in np.ndenumerate(counts):
        if not np.isnan(counts[j][i]):
            plt.text(i,
                     j,
                     str(int(counts[j][i])),
                     ha='center',
                     va='center',
                     size=6)

    plt.xticks(ticks=range(len(months)), labels=months, rotation=90)
    plt.yticks(ticks=range(len(days)), labels=days)

    plt.show()

def display_distribution(df):
    years = list(reversed(df["year"].unique()))
    plt.figure(figsize=(20, 8))
    plt.boxplot(list(map(lambda year: df[df["year"] == year]["count"], years)),
                labels=years)
    plt.show()

def count_messages_telegram(account,
                            counter=dict(),
                            path="./telegram.json",
                            sender=None):
    with open(path) as reader:
        msgs = json.load(reader)

        if type(sender) is str:
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

        return counter

counter = count_messages_facebook("stephanexu_rad3zuzd2q", sender=None)
count_messages_telegram("Stéphane", counter=counter, sender=None)

df = df_from_counter(counter)

display_distribution(df)
display_values_per_day(df)
