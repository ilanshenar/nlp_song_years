import csv
import collections
import tfidf
import gensim 

freq = {}

lyric_list = []
sentences = []

print ("?fuck.".strip(".,()!?"))

my_tfidf = tfidf.TfIdf()
with open('lyrics.csv', 'rb') as csv_lyrics:
    csv_reader = csv.reader(csv_lyrics, delimiter=',')
    for row in csv_reader:
        lyrics = row[5]
        my_tfidf.add_input_document(lyrics)
        lyric_list.append(lyrics)
        
        lines = lyrics.split("\n")
        for line in lines[1:]: 
            sentence = line.split(" ") 
            sentence = [word.strip(".,()!?") for word in sentence]
            sentences.append(sentence)
model = gensim.models.Word2Vec(sentences)
model.save("word2vec_output")







"""
for lyrics in lyric_list:         
    word_list = lyrics.split( )
    if "happy" in word_list: 
        t += 1
        for word in word_list:
            if word not in freq:
                freq[word] = 0.0
            freq[word] += 1.0
print(t) 
print(len(freq))
    
for word, key in freq.items():
    freq[word] *= my_tfidf.get_idf(word)
    
results = collections.OrderedDict(sorted(freq.items(),reverse=True, key= lambda t: t[1]))
i = 0
for word, val in freq.items(): 
    print(word)
    i += 1
    if i >= 50:
        break
"""
  
   