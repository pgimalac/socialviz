import math
import numpy as np
from matplotlib import pyplot as plt

# Returns the value for the given month and day, or NaN if there is no such value.
def get_value(df, day, month):
    try:
        return df[(df["year-month"] == month)
                  & (df["day"] == day)]["count"].iloc[0]
    except IndexError:
        return float("nan")

def display_values_per_day(df):
    months = sorted(reversed(df["year-month"].drop_duplicates()))
    days = list(range(1, 32))

    # Generate a bidimensional array, the first dimension is of size 31 (one per day), the second is dimension is year-month
    # There is probably a way to do that more efficiently (with groupby and such) but it works like this
    counts = [[get_value(df, day, month) for month in months] for day in days]

    counts = np.array(counts)

    plt.figure(figsize=(20, 10))
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
                     size=6)

    # Explicitly set x ticks as the list of year-month
    plt.xticks(ticks=range(len(months)), labels=months, rotation=90)
    # Explicitly set y ticks as the list of ints from 1 to 31
    plt.yticks(ticks=range(len(days)), labels=days)

    plt.show()

# Displays the distribution for each year (min, 1st quartile, median, 3rd quartile, max + outliers)
def display_distribution(df):
    years = list(reversed(df["year"].unique()))
    plt.figure(figsize=(20, 8))
    plt.boxplot(list(map(lambda year: df[df["year"] == year]["count"], years)),
                labels=years)
    plt.show()
