# rss-telegram-bot
Telegram Bot that would read rss fead and send it to you as messages

# command list
- help - to show help
- list - list your feeds (shortcut /ls)
- notify - manually update feeds (shortcut /n)
- list-filters - list exluded key words (shortcut /lf) i.e /lf myFeedName
- add-filter - add key word to exclude (shortcut /af) i.e /af myFeedName not interesting phrase

# pip dependencies
- python-telegram-bot
- feedparser
- tinydb

# how-to
- install python 
- install pip dependencies
- git clone
- create your telegram bot using @BotFather
- create file telegram_token and paste there token from previous step
- python bot.py
