import datetime as dt
import pandas as pd

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
