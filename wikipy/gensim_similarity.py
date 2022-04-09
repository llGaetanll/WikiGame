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
wiki_vectors = gensim.downloader.download('fasttext-wiki-news-subwords-300')
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
