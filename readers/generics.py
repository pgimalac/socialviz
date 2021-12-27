import sys
import pandas as pd
import datetime as dt

# Generates a dataframe from the time list
# and add helper columns
def df_from_list(msgs):
    if not msgs:
        print("No message found")
        sys.exit(0)

    df = pd.DataFrame(msgs, columns=["time"])
    df.set_index("time", inplace=True)
    df.sort_index(inplace=True)

    # Generate helper columns
    df["year"] = df.index.to_series().map(lambda time: time.year)
    df["year-month"] = df.index.to_series().map(
        lambda time: f"{time.year}-{time.month:02}")
    df["month"] = df.index.to_series().map(lambda time: time.month)
    df["day"] = df.index.to_series().map(lambda time: time.day)
    df["hour"] = df.index.to_series().map(lambda time: time.hour)
    df["date"] = df.index.to_series().map(lambda time: time.date())

    return df

# Initiate generics command line parameters
def init(parser):
    parser.add_argument(
        '--no-attachs',
        action='store_false',
        help="if specified, attachments are not counted as messages")
    parser.add_argument(
        '--multi-attachs',
        action='store_true',
        help=
        "if specified, multiple attachments sent at once are counted as several messages"
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help="count messages sent by the given accounts accross all chats")
