# %%
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import gensim.models
import gensim.downloader
# %%
MODEL = "2017_eng_wiki_skipgram/model.bin"

word_vectors = gensim.models.KeyedVectors.load_word2vec_format(MODEL, binary=True)

# %%
print(word_vectors.most_similar("china_PROPN"))
# %%
# wiki_vectors = gensim.downloader.download('fasttext-wiki-news-subwords-300')
# %%
wiki_vectors.most_similar("china")
# %%
def most_similar(model, word):
    for term in model.index_to_key:
        if word in term:
            return (term, model.most_similar(term))
# %%
most_similar(word_vectors, 'china')
# %%
MODEL_2 = "wiki-news-300d-1M.vec"

news_vectors = gensim.models.KeyedVectors.load_word2vec_format(MODEL_2)
# %%
news_vectors.n_similarity(["Einstein"], ["Kardashian", "Kim"])
# %%
def rank_similarity(model, target, terms):
    """returns a sorted list of (word, similarity) tuples.
    
    terms should be underscore separated titles
    """
    output = dict()
    for title in terms:
        output[title] = model.n_similarity(target, title.split('_'))

    return sorted(output.items(), key=lambda x: x[1], reverse=True)
