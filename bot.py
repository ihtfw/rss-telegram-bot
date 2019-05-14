import logging

import sys
import sched
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update, Bot, ParseMode

import feedparser

from db import DB
from chat import Chat, Feed
from notifier import Notifier

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

db = DB()

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot : Bot, update : Update):
    """Send a message when the command /start is issued."""        
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')


def help(bot : Bot, update : Update):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Help!')

def notifyNew(bot : Bot, update : Update):      
    chat_id = update.message.chat_id
    chat = db.getchat(chat_id)    
    
    notifier: Notifier = Notifier(bot, chat)
    any: bool = notifier.notify()
    
    if not any:
        bot.send_message(chat_id=chat_id, text="No updates")
        return

    db.update(chat)    

def listFeeds(bot : Bot, update : Update):
    """List all availible feeds"""    
    chat_id = update.message.chat_id
    chat = db.getchat(chat_id)
    if len(chat.feeds) == 0:
        bot.send_message(chat_id=chat_id, text="No feeds yet!")
        return
        
    for feed in chat.feeds:                
        bot.send_message(chat_id=chat_id, text=feed.key + ':' + feed.url)


def handleMessage(bot : Bot, update : Update):
    """Echo the user message."""
    msg: str = update.message.text    
    chat_id = update.message.chat_id

    args = msg.split(' ')
    if len(args) != 2:        
        bot.send_message(chat_id=chat_id, text="Should be two args: name url")
        return

    key = args[0]
    url = args[1]    

    if not url.startswith("http"):        
        bot.send_message(chat_id=chat_id, text="Please provide link to rss feed!")
        return

    bot.send_message(chat_id=chat_id, text="Testing if it's rss feed...")

    try:        
        newsFeed = feedparser.parse(url)
        if newsFeed is None or newsFeed.entries is None or len(newsFeed.entries) == 0:    
            bot.send_message(chat_id=chat_id, text="Not a rss feed..")
            return
    except:
        problem = sys.exc_info()[0]
        bot.send_message(chat_id=chat_id, text="Not a rss feed.. " + problem)
        return

    chat = db.getchat(chat_id)
    chat.addfeed(Feed(key, url))
    
    db.update(chat)
    
    bot.send_message(chat_id=chat_id, text="Added!")

def error(bot : Bot, update : Update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)

def notificationCycle(bot: Bot, sc):     
    try:
        for chat in db.allChats():
            try:       
                notifier: Notifier = Notifier(bot, chat)
                any: bool = notifier.notify()        
                if any:                
                    db.update(chat)   
            except:
                problem = sys.exc_info()[0]
                logger.error('error in cycle for ' + chat.id + ' ' + problem)
    except:        
        bigproblem = sys.exc_info()[0]
        logger.error('error in cycle' + bigproblem)
        
    sc.enter(5 * 60, 1, notificationCycle, (bot, sc,))
    
def setupNotification(bot: Bot):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(5 * 60, 1, notificationCycle, (bot, s,))
    s.run()

def main():
    token: str = ''
    try:
        file = open("telegram_token", "r") 
        token = file.read() 
        file.close()
    except FileNotFoundError:
        logger.error('file telegram_token not found!')
        return

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", listFeeds))
    dp.add_handler(CommandHandler("ls", listFeeds))
    dp.add_handler(CommandHandler("notify", notifyNew))
    dp.add_handler(CommandHandler("n", notifyNew))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, handleMessage))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    setupNotification(dp.bot)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()