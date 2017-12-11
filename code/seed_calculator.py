from gensim.models import Word2Vec as w2v

emots = ["angry", "disgust", "happy", "horror", "sad", "surprise"]

model = w2v.load("word2vec_output")
for word in emots: 
    print (word)
    #print ([x[0] for x in model.wv.most_similar(positive=[word], topn = 50)])
    print (model.wv.most_similar(positive=[word], topn = 50))
    print 
    print (model.wv.most_similar_cosmul(positive=[word], topn = 50))
    print ("_______________________________")