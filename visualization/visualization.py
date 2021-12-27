import math
import datetime as dt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

DEFAULT_WIDTH = 20
DEFAULT_HEIGHT = 10

# Iterates from first to last inclusive, with the given step.
def iterdate(first, last, step=dt.timedelta(days=1)):
    while first <= last:
        yield first
        first += step

def itermonth(first, last):
    year = first.year
    month = first.month
    while year <= last.year and (year != last.year or month <= last.month):

        yield f"{year}-{month:02}"

        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

def count_by(df, by, fill=True):
    grouped = df.groupby([by])[by].count().rename_axis("count")

    if fill:
        # Generate range of all values
        first = min(df.date)
        last = max(df.date)
        allvalues = None
        if by == "year-month":
            itermonth(min(df.date), max(df.date))
        elif by == "year":
            allvalues = range(min(df.year), max(df.year) + 1)
        elif by == "day":
            if first.year == last.year and first.month == last.month:
                allvalues = range(min(df.day), max(df.day))
            else:
                allvalues = range(1, 32)
        elif by == "date":
            allvalues = iterdate(min(df.date), max(df.date))
        elif by == "month":
            if first.year == last.year:
                allvalues = range(min(df.month), max(df.month))
            else:
                allvalues = range(1, 13)
        elif by == "hour":
            allvalues = range(24)

        # Fill missing values with given range
        if allvalues is not None:
            missing = pd.Series(index=set(allvalues).difference(grouped.index))
            print(missing)
            grouped = grouped.append(missing).fillna(0)

    grouped.sort_index(inplace=True)
    return grouped

# Returns the value for the given month and day, or NaN if there is no such value.
def get_value(df, day, month):
    try:
        return df[(df["year-month"] == month)
                  & (df["day"] == day)]["count"].iloc[0]
    except IndexError:
        return float("nan")

def display_values_per_day(df,
                           width=DEFAULT_WIDTH,
                           height=DEFAULT_HEIGHT,
                           labelrotate=False):
    df = count_by(df, "date")
    df["year-month"] = map(
        df.index.to_series().map(lambda date: f"{date.year}-{date.month:02}"))
    df["day"] = map(df.index.to_series().map(lambda date: date.day))

    rotation = 0
    if labelrotate:
        rotation = 90
    months = sorted(reversed(df["year-month"].drop_duplicates()))
    days = list(range(1, 32))

    # Generate a bidimensional array, the first dimension is of size 31 (one per day), the second is dimension is year-month
    # There is probably a way to do that more efficiently (with groupby and such) but it works like this
    counts = [[get_value(df, day, month) for month in months] for day in days]

    counts = np.array(counts)

    plt.figure(figsize=(width, height))
    # Use the log to determine the color of the tile
    plt.imshow([[math.log(1 + x) for x in y] for y in counts],
               interpolation='none',
               aspect="auto",
               vmax=6.5)

    # Add the int values as labels on each tile
    for (j, i), _ in np.ndenumerate(counts):
        if not np.isnan(counts[j][i]):
            plt.text(i,
                     j,
                     str(int(counts[j][i])),
                     ha='center',
                     va='center',
                     size=6,
                     rotation=rotation)

    # Explicitly set x ticks as the list of year-month
    plt.xticks(ticks=range(len(months)), labels=months, rotation=90)
    # Explicitly set y ticks as the list of ints from 1 to 31
    plt.yticks(ticks=range(len(days)), labels=days)

    plt.show()

def display_count_hour(df, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    plt.figure(figsize=(width, height))
    plt.hist(df["hour"], bins=range(25))
    plt.xticks(ticks=range(24), labels=range(24))
    plt.show()

# Displays the distribution for each year/month (min, 1st quartile, median, 3rd quartile, max + outliers)
def display_distribution(df, by, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    uniqueby = sorted(df[by].unique())
    df = count_by(df, by)
    df["year"] = map(df.index.to_series().map(lambda date: date.year))
    df["year-month"] = map(
        df.index.to_series().map(lambda date: f"{date.year}-{date.month:02}"))

    plt.figure(figsize=(width, height))
    plt.boxplot(list(
        map(lambda unique: df[df[by] == unique]["count"], uniqueby)),
                labels=uniqueby)
    plt.xticks(ticks=range(1, len(uniqueby) + 1), labels=uniqueby, rotation=90)
    plt.show()

displays = [("display-ydistrib",
             lambda df, w, h, _: display_distribution(df, "year", w, h),
             "display the yearly distribution of messages"),
            ("display-mdistrib",
             lambda df, w, h, _: display_distribution(df, "year-month", w, h),
             "display the monthly distribution of messages"),
            ("display-counter", display_values_per_day,
             "display the number of messages for each day"),
            ("hour-count", lambda df, w, h, _: display_count_hour(df, w, h),
             "display the number of messages sent each hour of the day")]

def init(parser):
    group = parser.add_argument_group(
        "displays",
        "the various possible displays. If none is selected, all are displayed"
    )
    for name, _, helper in displays:
        group.add_argument(f"--{name}", action='store_true', help=helper)

    group.add_argument(
        "--figsize-w",
        help=
        f"the width of the generated plots in inch. Defaults to {DEFAULT_WIDTH}",
        type=int,
        action="store",
        default=DEFAULT_WIDTH)
    group.add_argument(
        "--figsize-h",
        help=
        f"the height of the generated plots in inch. Defaults to {DEFAULT_HEIGHT}",
        type=int,
        action="store",
        default=DEFAULT_HEIGHT)
    group.add_argument(
        "--rotate-labels",
        help=
        "rotate the labels of the heatmap. Convenient for big values or big timelapse",
        action="store_true")

def display(df, values):
    any_specified = any(
        map(lambda display: values[display[0].replace('-', '_')], displays))

    for name, display, _ in displays:
        if not any_specified or values[name.replace('-', '_')]:
            display(df, values["figsize_w"], values["figsize_h"],
                    values["rotate_labels"])
