from gensim.models import KeyedVectors


title1 = "Greatest_Hits_(1993_Richard_Marx_album)"
title2 = "The_Best_of_Richard_Marx"


MODEL_BIN = 'Bots/Model/wiki-news-300d-1M.vec'
#MODEL = KeyedVectors.load_word2vec_format(MODEL_BIN)
#MODEL.save('Bots/Model/computed.d2v')
MODEL = KeyedVectors.load('Bots/Model/computed.d2v')
model_keys = MODEL.index_to_key

title1_tokens = title1.split('_')
title1_tokens = list(filter(lambda x: x in model_keys, title1_tokens))


title2_tokens = title2.split('_')
title2_tokens = list(filter(lambda x: x in model_keys, title2_tokens))


print(MODEL.n_similarity(title1_tokens, title2_tokens))

