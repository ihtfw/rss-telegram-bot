from tinydb import TinyDB, Query

from chat import Chat, Feed


class DB:    
    def __init__(self):
        self.db = TinyDB('db.json', sort_keys=True, indent=4)
        self.chatquery = Query()

    def allChats(self):
        for db_chat in self.db:
            chat = self.from_json(db_chat)
            yield chat

    def getchat(self, chat_id) -> Chat:
        """Would return existing or create new one"""
        db_chat = self.db.get(self.chatquery.id == chat_id)    
        chat = None
        if db_chat == None:
            chat = Chat(chat_id)
            jObj = self.to_json(chat)
            self.db.insert(jObj)
        else:
            chat = self.from_json(db_chat)
        
        return chat

    def update(self, chat: Chat):
        jObj = self.to_json(chat)
        self.db.update(jObj, self.chatquery.id == chat.id)
    
    def to_json(self, chat: Chat):
        json = {'id': chat.id, 'feeds': []}
        for feed in chat.feeds:
            json['feeds'].append({'key': feed.key, 'url': feed.url, 'lastUpdate': feed.lastUpdate})

        return json

    def from_json(self, json):
        chat = Chat(json['id'])
        for jFeed in json['feeds']:
            feed: Feed = Feed(jFeed['key'], jFeed['url'])
            feed.lastUpdate = jFeed['lastUpdate']
            chat.addfeed(feed)
        return chat

