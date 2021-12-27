# socialviz
Message visualizator for various social networks.

## Social networks supported
#### Facebook Messenger
Export your data from the Facebook interface, in json format.

The result should be a folder `messages/inbox/`, in which each sub-folder corresponds to a conversation, and contains one or several json files.

The `fbpath` parameter is the path to the `inbox` directory, `fbaccount` is the name of the subfolder corresponding to a conversation, and each `fbsender` must be given like it appears in `sender_name` in messages, or in `name` in `participants`.

#### Telegram
Export your data from the Telegram interface, in json format.

The result should be a file `results.json`, containing the list of conversation, and each conversation contains the list of messages.

The `tgpath` parameter is the path to the `results.json` file, `tgaccount` is the name of the conversation like it appears in `name`, and each `tgsender` must be given like it appears in `name` in messages.

#### Discord
Exporting your data from the Discord interface will only give your own messages and not those sent to you.
Thus, we use [https://github.com/Tyrrrz/DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) to export the conversations in json format.

The result should be a set of json files, one per conversation.

The `dcpath` parameter is the path to the directory containing those json files, `dcaccount` is the name of one such json file, and each `dcsender` must be given like it appears in the `name` field of the `author` dictionnary in the message.

## Usage
Run `python socialviz.py --help` to see the list of command line arguments.

#### Facebook only, for all senders
If the inbox directory is located at `./messages/inbox`, and we want to count messages in the directory named `johnsmith_fO2hnrKt`:
```sh
python socialviz.py --fbpath "./messages/inbox" --fbaccount "johnsmith_fOhnrKt"
```

#### Telegram only, for senders "John" and "Joe"
If the json file is located at `./telegram.json`, and we want to count messages in the chat named `John`:
```sh
python socialviz.py --tgaccount "John" --tgpath "./telegram.json" --tgsender "John" --tgsender "Joe"
```

#### Facebook and Telegram, no attachments, plot only the distribution
```sh
python socialviz.py --no-attachs --fbaccount "johnsmith_fOhnrKt" --tgaccount "John" --display-distribution
```
#### All messages sent by the given accounts, specify figure size and rotate labels
```sh
python socialviz.py --all --fbsender "John Smith" --tgsender "John Smith" --dcsender "johnsmith" --figsize-w 30 --figsize-h 15 --rotate-labels
```

## Plots
The possible types of plots are:
- plot the yearly distribution of daily count of messages
![example of distribution plot](./assets/distribution.png)

- plot a 2D heatmap containing the daily counts of messages, for each day and year-month
![example of heatmap](./assets/heatmap.png)

## TODO
- [ ] Handle Skype data
- [ ] Refactor command line arguments with actual subcommands
- [ ] Refactor readers to add one more easily
- [ ] Refactor heatmap visualization to be more efficient
