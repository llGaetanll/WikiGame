import bot
from plaintext import Plaintext
from bs4 import BeautifulSoup

# Page functionally replaced by Plaintext

# class Page:
#     """
#     A wikipedia page
#     """
#     def __init__(self, plaintext):
#         """This would probably make more sense if it took HTML as input"""
#         self.plaintext = plaintext
#         self.title = title
#         self.url = "https://en.wikipedia.org/wiki/" + title
#         self.text = None # query to get plaintext of article
#         self.links = [None] # manipulate text to get links, save as titles
#         self.backlinks = None # access the 'links to this page' in the tools on the sidebar


class Game:
    def __init__(self, path):
        """
        Initialize a game.
        
        path: a list of Plaintext objects representing the random walk taken to create the start and end points of the game. If intermediate pages are not passed, list should 
        """
        self.start = path[0]
        self.target = path[-1]
        self.current_page = path[0]
        self.encountered = [path[0]] # pages encountered (as Plaintext objects)
    
    def next_move(self, plaintext):
        """
        return the title of the next move page. This method should include (or at least call) the actual logic of the bot.
         """
        # incorporating the newly received page
        self.current_page = plaintext
        self.encountered.append(plaintext)

        link_ranking = bot.rank_similarity(self.end, self.current_page.links)

        for title, _ in link_ranking:
            if title == self.target:
                return title # if the target is in the list of links, return it
            if title in self.encountered:
                continue # avoiding loop
            self.encountered.append(title)
            return title # return the first link that hasn't been encountered
        return "FAILED" # if there are no new links