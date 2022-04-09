
class Page:
    """
    A wikipedia page
    """
    def __init__(self, title):
        """This would probably make more sense if it took HTML as input"""
        self.title = title
        self.url = "https://en.wikipedia.org/wiki/" + title
        self.text = None # query to get plaintext of article
        self.links = [None] # manipulate text to get links
        self.backlinks = None # access the 'links to this page' in the tools on the sidebar


class Game:
    def __init__(self, path):
        """
        Initialize a game.
        
        path: a list of Page objects representing the random walk taken to create the start and end points of the game.
        """
        self.start = path[0]
        self.end = path[-1]
        self.current_page = path[0]
        self.encountered = [path[0]] # pages yet encountered
    
    def next_move(self):
        """
        return the title of the next move page. This method should include (or at least call) the actual logic of the bot.
        
        Should at some point access self.encountered to avoid loops.
         """
        return "NOT IMPLEMENTED"
