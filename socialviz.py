import argparse
from readers import generics, facebook, telegram, discord
from visualization import visualization as viz

parser = argparse.ArgumentParser(
    description='Reads messages from various social medias and generates plots.'
)

# Add command line parameters
generics.init(parser)
facebook.init(parser)
telegram.init(parser)
discord.init(parser)
viz.init(parser)

# Parse
args = parser.parse_args()
values = vars(args)

# Init message list
msgs = []

# Run
facebook.parse(msgs, values)
telegram.parse(msgs, values)
discord.parse(msgs, values)

# Generate full dataframe with helper columns
df = generics.df_from_list(msgs)

# Display
viz.display(df, values)
