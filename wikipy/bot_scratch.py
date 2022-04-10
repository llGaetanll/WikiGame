# %%
import re
import Plaintext
import requests
from bs4 import BeautifulSoup
import gensim.models

# %%
MODEL_BIN = "wiki-news-300d-1M.vec"

#MODEL = gensim.models.KeyedVectors.load_word2vec_format(MODEL_BIN)

# %%
def rank_similarity(target, terms):
    """returns a sorted list of (word, similarity) tuples.

    terms should be underscore separated titles
    """
    output = dict()
    for title in terms:
        output[title] = MODEL.n_similarity(target, title.split('_'))

    return sorted(output.items(), key=lambda x: x[1], reverse=True)


# %%
def get_linked_pages(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    reg = re.compile('\/wiki\/.*')
    
    titles = []
    for link in soup.find_all('a', href=True, title=True):
        if reg.match(link["href"]):
            titles.append(link["title"].replace(' ','_'))
    
    return titles
    

# %%
def move(title, dest):
    links = get_linked_pages("https://en.wikipedia.org/wiki/" + title)

    link_ranking = bot.rank_similarity(dest, links)

    return link_ranking[0][0]


