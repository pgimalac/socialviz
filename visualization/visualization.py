import math
import numpy as np
from matplotlib import pyplot as plt

DEFAULT_WIDTH = 20
DEFAULT_HEIGHT = 10

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

# Displays the distribution for each year (min, 1st quartile, median, 3rd quartile, max + outliers)
def display_distribution(df,
                         width=DEFAULT_WIDTH,
                         height=DEFAULT_HEIGHT,
                         labelrotate=False):
    years = list(df["year"].unique())
    plt.figure(figsize=(width, height))
    plt.boxplot(list(map(lambda year: df[df["year"] == year]["count"], years)),
                labels=years)
    plt.show()

displays = [("display-distribution", display_distribution,
             "display the yearly distribution of the messages"),
            ("display-counter", display_values_per_day,
             "display the number of messages for each day")]

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
            display(df,
                    width=values["figsize_w"],
                    height=values["figsize_h"],
                    labelrotate=values["rotate_labels"])
