import gensim.models

MODEL_BIN = "wiki-news-300d-1M.vec" # this file is not currently in the repo because its 2.26GB

# takes forever 
MODEL = gensim.models.KeyedVectors.load_word2vec_format(MODEL_BIN)

def rank_similarity(target, terms):
    """returns a sorted list of (word, similarity) tuples.
    
    terms should be underscore separated titles
    """
    output = dict()
    for title in terms:
        output[title] = MODEL.n_similarity(target, title.split('_'))

    return sorted(output.items(), key=lambda x: x[1], reverse=True)
