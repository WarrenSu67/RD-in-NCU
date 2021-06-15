class ArticleOutline:
    def __init__(self, category, news, link):
        super().__init__()

        self.category = category
        self.news = news
        self.link = link

    def toJSON(self):
        return {"category": self.category, "news": self.news, "link": self.link}
    
    def printJson(self):
        print({"category": self.category, "news": self.news, "link": self.link})