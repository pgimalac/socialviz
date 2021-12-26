import argparse

from readers import generics, facebook, telegram
from visualization import visualization as viz

parser = argparse.ArgumentParser(
    description='Reads messages from various social medias and generates plots.'
)

# Add command line parameters
generics.init(parser)
facebook.init(parser)
telegram.init(parser)
viz.init(parser)

# Parse
args = parser.parse_args()
values = vars(args)

# Init message counter
counter = {}

# Run
facebook.parse(counter, values)
telegram.parse(counter, values)

# Generate dataframe from counter
df = generics.df_from_counter(counter)

# Display
viz.display(df, values)
