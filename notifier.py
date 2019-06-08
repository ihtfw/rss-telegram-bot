import time
import feedparser

from telegram import Bot, ParseMode

from chat import Chat, Feed

class Notifier:
    def __init__(self, bot: Bot, chat: Chat):
        self.chat = chat
        self.bot = bot

    def formatAsHtml(self, text: str):
        return text.replace('<br />', '\n').replace('<br/>', '\n').replace('&nbsp;', ' ').replace('&middot;', '·').replace('&middot;', '·').replace('&amp;', '&').replace('&bull;', '•')

    def buildText(self, entry) -> str:
        return '<b>' + entry.title + '</b>\n\n' + self.formatAsHtml(entry.summary)
    
    def send(self, entry):
        self.bot.send_message(chat_id=self.chat.id, text=self.buildText(entry), parse_mode=ParseMode.HTML, disable_web_page_preview=True)   

    def isFiltered(self, feed: Feed, entry) -> bool:
        for filter in feed.filterBy:
            title: str = entry.title.lower()
            summary : str = entry.summary.lower()
            
            if title.find(filter.lower()) >= 0:
                return True

            if summary.find(filter.lower()) >= 0:
                return True
        
        return False

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
                        if not self.isFiltered(feed, entry):
                            self.send(entry)                        
                            feed.lastUpdate = curTime
                            any = True

            except:
                continue
        
        return any