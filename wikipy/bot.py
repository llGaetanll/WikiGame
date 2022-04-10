
from flask import Flask, request
import bot
import re
import gensim.models


# this file is not currently in the repo because its 2.26GB
MODEL_BIN = "wiki-news-300d-1M.vec"

# takes forever
MODEL = gensim.models.KeyedVectors.load_word2vec_format(MODEL_BIN)

app = Flask(__name__)


def rank_similarity(target, terms):
    """returns a sorted list of (word, similarity) tuples.

    terms should be underscore separated titles
    """
    output = dict()
    for title in terms:
        output[title] = MODEL.n_similarity(target, title.split('_'))

    return sorted(output.items(), key=lambda x: x[1], reverse=True)

def rank_similarity_to_page(target, terms):
    """returns a sorted list of (word, similarity) tuples, comparing to the plaintext of the target page. target should be a Plaintext object.

    terms should be underscore separated titles
    """
    output = dict()
    for title in terms:
        output[title] = MODEL.n_similarity(target.text.split(' '), title.split('_'))

    return sorted(output.items(), key=lambda x: x[1], reverse=True)
    
# API


@app.route("/", methods=['GET'])
def move():
    body = request.json

    # parsed page
    page = body.page

    # extract all links from parsed page
    links = re.findall(r'\|\|(\S+)\|\|', page)

    # destination page name
    dest = body.dest

    # compute ranking vector for links and destination
    link_ranking = bot.rank_similarity(dest, links)

    # return the highest ranked title
    return link_ranking[0][0]

    # for title, _ in link_ranking:
    #     if title == dest:
    #         return title # if the target is in the list of links, return it
    #     # if title in self.encountered:
    #     #     continue # avoiding loop
    #     # self.encountered.append(title)
    #     return title # return the first link that hasn't been encountered
    # return "FAILED" # if there are no new links

    # return "Hello, World!"




