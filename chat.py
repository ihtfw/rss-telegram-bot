from typing import List, Any

class Feed:
    def __init__(self, key: str, url: str):
        self.key = key
        self.url = url
        self.lastUpdate = None
    

class Chat:   
    def __init__(self, chat_id):
        self.id = chat_id
        self.feeds = []
    
    def addfeed(self, feed: Feed):
        self.feeds.append(feed)
        
    def addfeeds(self, feeds: []):
        for feed in feeds:
            self.addfeed(feed)