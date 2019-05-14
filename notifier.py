import time
import feedparser

from telegram import Bot, ParseMode

from chat import Chat, Feed

class Notifier:
    def __init__(self, bot: Bot, chat: Chat):
        self.chat = chat
        self.bot = bot

    def formatAsHtml(self, text: str):
        return text.replace('<br />', '\n').replace('<br/>', '\n')

    def buildText(self, entry) -> str:
        return '<b>' + entry.title + '</b>\n\n' + self.formatAsHtml(entry.summary)
    
    def send(self, entry):
        self.bot.send_message(chat_id=self.chat.id, text=self.buildText(entry), parse_mode=ParseMode.HTML, disable_web_page_preview=True)   

    def notify(self) -> bool:
        any: bool = False
        for feed in self.chat.feeds:
            try:      
                curTime = time.time()
                newsFeed = feedparser.parse(feed.url)
                if newsFeed is None or newsFeed.entries is None or len(newsFeed.entries) == 0:    
                    continue
                
                lastUpdateTime: time.struct_time = None
                if feed.lastUpdate != None:
                    lastUpdateTime = time.gmtime(feed.lastUpdate)
                            
                for entry in newsFeed.entries:
                    pTime: time.struct_time = entry.published_parsed
                    if lastUpdateTime == None or pTime > lastUpdateTime:
                        self.send(entry)                        
                        feed.lastUpdate = curTime
                        any = True

            except:
                continue
        
        return any