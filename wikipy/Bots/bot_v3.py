# %%
import re
import requests
from bs4 import BeautifulSoup
from gensim.models import KeyedVectors

# bot no longer vists pages even too SIMILAR to previous pages

# METAPARAMETER in [0,1]
cutoff = 0.8


# %%
MODEL_BIN = 'Model/wiki-news-300d-1M.vec'
#MODEL = KeyedVectors.load_word2vec_format(MODEL_BIN)
#MODEL.save('Model/computed.d2v')
MODEL = KeyedVectors.load('Model/computed.d2v')


# %%
def get_linked_pages(title):
    url = "https://en.wikipedia.org/wiki/" + title
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    reg = re.compile('\/wiki\/.*')
    
    titles = []
    for link in soup.find_all('a', href=True, title=True):
        if reg.match(link["href"]):
            titles.append(link["title"].replace(' ','_'))
    
    return titles
    
# %%
model_keys = MODEL.index_to_key

def tokenize_wikiterm(term):
    tokens = term.replace("(", "").replace(")", "").split()
    tokens = [x for x in tokens if x in model_keys]
    list(filter(lambda x: x in model_keys, tokens))
    return tokens



def rank_similarity(target, terms, visited):
    target_tokens = target.split('_')
    target_tokens = list(filter(lambda x: x in model_keys, target_tokens))
    
    output = dict()
    terms = list(filter(lambda x: not x in visited, terms))
    for poten in terms:
        poten_tokens = poten.split('_')
        poten_tokens = list(filter(lambda x: x in model_keys, poten_tokens))

        similar = False

        for prev in visited:
            if similar:
                continue
            prev_tokens = prev.split('_')
            prev_tokens = list(filter(lambda x: x in model_keys, prev_tokens))
            if len(prev_tokens) == 0 or len(poten_tokens) == 0:
                continue
            similar = (cutoff < MODEL.n_similarity(prev_tokens, poten_tokens))


        if similar or len(poten_tokens) == 0:
            continue

        output[poten] = MODEL.n_similarity(target_tokens, poten_tokens)

    return sorted(output.items(), key=lambda x: x[1], reverse=True)



# %%
def move(title, dest, visited):
    links = get_linked_pages(title)
    link_ranking = rank_similarity(dest, links, visited)

    return link_ranking[0][0]


# %%
def bot_walk(n, curr, dest, path):
    path.append(curr)
    if n == 0:
        return path
    if curr == dest:
        return path
    else:
        next = move(curr, dest, path)
        return bot_walk(n-1, next, dest, path)



# %%
path = bot_walk(18, "Kim_Kardashian", "Albert_Einstein", list())
print(path)

