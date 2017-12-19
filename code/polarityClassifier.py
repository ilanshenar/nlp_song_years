from __future__ import division
import math
import sklearn
from collections import Counter

emotions = ["angry", "disgust", "happy", "horror", "sad", "surprise"]
seeds = {"angry" : ["angry", "ugly", "mad", "anxious", "jaded", "ignorant", "frustrated", "jealous", "emotional", "insecure", "hungry", "confused", "cynical"], 
         "disgust" : ["disgust","scorn", "contempt", "disdain", "hatred", "guilt", "bitterness", "apathy", "anxiety", "fury", "vile", "anguish"], 
         "happy" : ["happy", "glad", "lucky", "alive", "good", "pleased", "satisfied", "thankful", "fine", "complete", "grateful", "content", "perfect"], 
         "horror" : ["horror", "chaos", "terror", "delusion", "gloom", "plague", "violence", "blackness", "bloodshed", "cruelty", "madness"],
         "sad" :  ["sad", "lonely", "miserable", "depressed", "boring", "tragic", "pathetic", "hopeless", "weird", "helpless"], 
         "surprise" : ["surprise", "warning", "shame", "mistake", "fool", "joke", "mystery", "thrill", "gift", "coincidence", "chance"]}

class PolarityClassifier:
    global emotions, seeds
    
    ML_classifiers = [sklearn.linear_model.Perceptron(), sklearn.svm.SVC(), sklearn.neighbors.KNeighborsClassifier(), sklearn.linear_model.LogisticRegression(), sklearn.naive_bayes.GaussianNB()]
    
    def __init__(self):
        self.song_count = 0
        self.emotion_count = {e: 0 for e in emotions}
        self.total_lyrics_count = 0
        self.lyric_count = {}
        self.emotion_lyric_count = {e : {} for e in emotions}
        self.emotion_PMI_lyric = {e : {} for e in emotions}
       
    def generateEmotionVec(X):
        song_emotion_PMI = []
        i = 0
        for x in X: 
            song_emotion_PMI.append([])
            for emot in emotions: 
                PMI_sum_emot = 0
                for lyric in x.split():
                    if lyric not in self.emotion_PMI_lyric[emot]: 
                        continue
                    PMI_sum_emot +=  self.emotion_PMI_lyric[emot][lyric]
                self.song_emotion_PMI[i].append(PMI_sum_emot)
            i += 1
        return song_emotion_PMI
    
    def fit(self, X, y):
        
        for x in X:     
            lyric_list = x.split()
            is_emot = {e : False for e in emotions}
            for emot in emotions: 
                if any(x in lyric_list for x in seeds[emot]):
                    is_emot[emot] = True

            for lyric in lyric_list: 
                self.total_lyrics_count += 1
                for emot in emotions: 
                    if lyric in seeds[emot]:
                        self.emotion_count[emot] += 1
                if lyric not in self.lyric_count:
                    self.lyric_count[lyric] = 1
                    for emot in emotions: 
                        self.emotion_lyric_count[emot][lyric] = 1    
                else:
                    self.lyric_count[lyric] += 1
                    for emot in emotions: 
                        if is_emot[emot]:
                            emotion_lyric_count[emot][lyric] += 1
                         
        for words in self.lyric_count:
            for emot in emotions: 
                co_occ = self.emotion_lyric_count[emot][lyric] / total_lyric_count
                occ_x = self.lyric_count[lyric] / total_lyric_count
                occ_y = emotion_count[emot] / total_lyric_count
                self.emotion_PMI_lyric[emot][lyric] = math.log(co_occ / (occ_x * occ_y))
        
        emot_vec = generateEmotionVec(X)
        
        for classifier in ML_classifiers:
            classifier.fit(emot_vec, y)
        
    def predict(X):
        pred = []
        
        emot_vec = generateEmotionVec(X)
        pred_vec = []
        
        i = 0
        for classifier in ML_classifiers:
            pred_vec.append([])
            pred_vec[i].append(classifier.predict(emot_vec)
            i += 1
        
        print (len(pred_vec))                       
        for i in range(len(X)):
            preds = [pred_vec[u][i] for u in range(len(pred_vec))]
            b = Counter(preds)
            pred.append(b.most_common(1))                   
                               
        return pred

                               
        
                
            
            
        