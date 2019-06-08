from typing import List, Any

class Feed:
    def __init__(self, key: str, url: str):
        self.key = key
        self.url = url
        self.lastUpdate = None
        self.filterBy = []

    def addFilterBy(self, filterBy: []):
        if filterBy is None:
            return

        for filter in filterBy:
            self.filterBy.append(filter)

    def addFilterByItem(self, filterBy: str):
        if filterBy is None:
            return

        self.filterBy.append(filterBy)
    

class Chat:   
    def __init__(self, chat_id):
        self.id = chat_id
        self.feeds = []
    
    def addfeed(self, feed: Feed):
        self.feeds.append(feed)
        
    def addfeeds(self, feeds: []):
        for feed in feeds:
            self.addfeed(feed)

