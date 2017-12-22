from __future__ import division
import math
import sklearn
import numpy as np
from sklearn import linear_model
from sklearn import svm
from sklearn import neighbors
from sklearn import naive_bayes

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
    
    ML_classifiers = [sklearn.neighbors.KNeighborsClassifier(), sklearn.linear_model.LogisticRegression(), sklearn.naive_bayes.GaussianNB()]
    radius = 5
    
    def __init__(self):
        self.song_count = 0
        self.emotion_count = {e: 0 for e in emotions}
        self.total_lyric_count = 0
        self.lyric_count = {}
        self.emotion_lyric_count = {e : {} for e in emotions}
        self.emotion_PMI_lyric = {e : {} for e in emotions}
       
    def generateEmotionVec(self, X):
        song_emotion_PMI = []
        i = 0
        for x in X: 
            song_emotion_PMI.append([])
            for emot in emotions: 
                PMI_sum_emot = 0
                for lyric in x.split():
                    if lyric not in self.emotion_PMI_lyric[emot] or self.lyric_count[lyric] < 100: 
                        continue
                    PMI_sum_emot +=  self.emotion_PMI_lyric[emot][lyric]
                song_emotion_PMI[i].append(PMI_sum_emot)
                
                max_emot = max(song_emotion_PMI[i])
                song_emotion_PMI[i] = [y / max_emot for y in song_emotion_PMI[i]]
                
            i += 1
        return song_emotion_PMI
    
    def fit(self, X, y):
        
        for x in X:     
            lyric_list = x.split()
            num_words = len(lyric_list)
            
            for i in range(num_words):
                lyric = lyric_list[i]
                self.total_lyric_count += 1
                
                if lyric not in self.lyric_count:
                    self.lyric_count[lyric] = 1
                    for emot in emotions: 
                        self.emotion_lyric_count[emot][lyric] = 1 
                
                self.lyric_count[lyric] += 1
                local_lyrics = lyric_list[max(0, i - self.radius) : min(num_words, i + self.radius)]
                for emot in emotions: 
                    if lyric in seeds[emot]:
                        self.emotion_count[emot] += 1
                    if any(x in local_lyrics for x in seeds[emot]):
                        self.emotion_lyric_count[emot][lyric] += 1
            
            
            
            
            
            #is_emot = {e : False for e in emotions}
            #for emot in emotions: 
            #    if any(x in lyric_list for x in seeds[emot]):
            #        is_emot[emot] = True

            #for lyric in lyric_list: 
            #    self.total_lyric_count += 1
            #    for emot in emotions: 
                    
            #    if lyric not in self.lyric_count:
            #        self.lyric_count[lyric] = 1
            #        for emot in emotions: 
            #            self.emotion_lyric_count[emot][lyric] = 1    
            #    else:
            #        self.lyric_count[lyric] += 1
            #        for emot in emotions: 
            #            if is_emot[emot]:
            #                self.emotion_lyric_count[emot][lyric] += 1
                         
        for lyric in self.lyric_count:
            for emot in emotions: 
                co_occ = self.emotion_lyric_count[emot][lyric] / self.total_lyric_count
                occ_x = self.lyric_count[lyric] / self.total_lyric_count
                occ_y = self.emotion_count[emot] / self.total_lyric_count
                #print (lyric + ": " + emot + ": " + str(math.log(co_occ / (occ_x * occ_y))))
                self.emotion_PMI_lyric[emot][lyric] = math.log(co_occ / (occ_x * occ_y))
        
        
        emot_vec = self.generateEmotionVec(X)
        print (emot_vec)
        
        for classifier in self.ML_classifiers:
            classifier.fit(emot_vec, y)
        
    def predict(self, X):
        pred = []
        
        emot_vec = self.generateEmotionVec(X)
        pred_vec = [[] for j in range(len(X))]
        
        for classifier in self.ML_classifiers:
            p = classifier.predict(emot_vec)
            #print (p)
            for j in range(len(X)): 
                pred_vec[j].append(p[j]) 
        
        #print (len(pred_vec))                       
        for i in range(len(X)):
            counts = np.bincount(pred_vec[i])
            pred.append(np.argmax(counts))
                  
        #print (pred_vec)                       
        return pred
    
    

                               
        
                
            
            
        