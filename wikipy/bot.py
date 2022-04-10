# %%
from flask import Flask, request
import re
import gensim.models
# %%

# this file is not currently in the repo because its 2.26GB
MODEL_BIN = "wiki-news-300d-1M.vec"

# takes forever
MODEL = gensim.models.KeyedVectors.load_word2vec_format(MODEL_BIN)
# %%

app = Flask(__name__)

model_keys = MODEL.index_to_key


def tokenize_wikiterm(term):
    tokens = term.replace("(", "").replace(")", "").split()
    tokens = [x for x in tokens if x in model_keys]
    list(filter(lambda x: x in model_keys, tokens))

    return tokens


def rank_similarity(target, terms):
    """
    returns a sorted list of (word, similarity) tuples.
    terms should be underscore separated titles
    """

    target_tokens = tokenize_wikiterm(target)

    output = dict()
    for title in terms:
        title_tokens = tokenize_wikiterm(title)

        if len(title_tokens) == 0:
            continue

        output[title] = MODEL.n_similarity(target_tokens, title_tokens)

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
    body = request.get_json()

    # parsed page
    page = body['page']

    # destination page name
    dest = body['dest']

    # extract all links from parsed page
    links = re.findall(r'{{([^{}]*)\|([^{}]*)}}', page)
    link_dict = {x[0]: x[1] for x in links}

    # compute ranking vector for links and destination
    best_link = rank_similarity(dest, link_dict.keys())[0][0]

    return link_dict[best_link]


app.run(port=3001)
