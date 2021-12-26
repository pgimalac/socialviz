from readers import generics, facebook, telegram
from visualization import visualization as viz

counter = {}
facebook.count_messages("stephanexu_rad3zuzd2q", counter, sender=None)
telegram.count_messages("Stéphane", counter, sender=None)

df = generics.df_from_counter(counter)

viz.display_distribution(df)
viz.display_values_per_day(df)
