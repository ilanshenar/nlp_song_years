from __future__ import division
import numpy as np
import operator 
import math
import collections
import csv
from string import punctuation
import matplotlib.pyplot as plt


emotions = ["angry", "disgust", "happy", "horror", "sad", "surprise"]
year_span = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]
year_songs = {x : [] for x in year_span}

year_song_count = {x : 0 for x in year_span}
year_lyric_count = {x : {} for x in year_span}

year_emotion_lyric_count = {y : {e : {} for e in emotions} for y in year_span}
year_emotion_count = {y : {e : 1 for e in emotions} for y in year_span}


seeds = {"angry" : ["angry", "ugly", "mad", "anxious", "jaded", "ignorant", "frustrated", "jealous", "emotional", "insecure", "hungry", "confused", "cynical"], 
         "disgust" : ["disgust","scorn", "contempt", "disdain", "hatred", "guilt", "bitterness", "apathy", "anxiety", "fury", "vile", "anguish"], 
         "happy" : ["happy", "glad", "lucky", "alive", "good", "pleased", "satisfied", "thankful", "fine", "complete", "grateful", "content", "perfect"], 
         "horror" : ["horror", "chaos", "terror", "delusion", "gloom", "plague", "violence", "blackness", "bloodshed", "cruelty", "madness"],
         "sad" :  ["sad", "lonely", "miserable", "depressed", "boring", "tragic", "pathetic", "hopeless", "weird", "helpless"], 
         "surprise" : ["surprise", "warning", "shame", "mistake", "fool", "joke", "mystery", "thrill", "gift", "coincidence", "chance"]}

#angry_seeds = ["angry", "ugly", "mad", "anxious", "jaded", "ignorant", "frustrated", "jealous", "emotional", "insecure", "hungry", "confused", "cynical"]
#disgust_seeds = ["disgust","scorn", "contempt", "disdain", "hatred", "guilt", "bitterness", "apathy", "anxiety", "fury", "vile", "anguish"]
#happy_seeds = ["happy", "glad", "lucky", "alive", "good", "pleased", "satisfied", "thankful", "fine", "complete", "grateful", "content", "perfect"]
#horror_seeds = ["horror", "chaos", "terror", "delusion", "gloom", "plague", "violence", "blackness", "bloodshed", "cruelty", "madness"]
#sad_seeds = ["sad", "lonely", "miserable", "depressed", "boring", "tragic", "pathetic", "hopeless", "weird", "helpless"]
#surprise_seeds = ["surprise", "warning", "shame", "mistake", "fool", "joke", "mystery", "thrill", "gift", "coincidence", "chance"]
#add words like "warn", "anger", "terrorize"????

f = open("data.txt", "r")
data = [x.split(",") for x in f.read().split("\n")]
f.close()

for song in data: 
    
    if len(song) < 3:
        continue
    
    year = song[0]
    genre = song[1]
    lyrics = song[2]
    
    lyric_list = lyrics.split()
    
    year_song_count[year] += 1
    
    is_emot = {e : False for e in emotions}
    for emot in emotions: 
        if any(x in lyric_list for x in seeds[emot]):
            is_emot[emot] = True
            year_emotion_count[year][emot] += 1
    for lyric in lyric_list: 
        if lyric not in year_lyric_count[year]:
            year_lyric_count[year][lyric] = 1 
            for emot in emotions: 
                year_emotion_lyric_count[year][emot][lyric] = 1
        else:
            year_lyric_count[year][lyric] += 1
        for emot in emotions: 
            if is_emot[emot]:
                year_emotion_lyric_count[year][emot][lyric] += 1

print("Polarity Frequencies Calculated")                
                
year_emotion_PMI_lyric = {y : {e : {} for e in emotions} for y in year_span}
song_emotion_PMI = {}
year_emotion_PMI = {}
          
for song in data: 
    if len(song) < 3:
        continue
    
    year = song[0]
    lyrics = song[2].split()
    for emot in emotions:   
        for lyric in lyrics:     
            co_occ = year_emotion_lyric_count[year][emot][lyric] / year_song_count[year]
            occ_x = year_lyric_count[year][lyric] / year_song_count[year]
            occ_y = year_emotion_count[year][emot] / year_song_count[year]
            year_emotion_PMI_lyric[year][emot][lyric] = math.log(co_occ / (occ_x * occ_y))
            
print("Word Polarities Calculated")            

max_PMI_emot = {e : -10000 for e in emotions} 

i = 0            
for song in data:
    if len(song) < 3:
        continue
    
    year = song[0]
    lyrics = song[2]
    song_emotion_PMI[i] = {}
    if year not in year_emotion_PMI:
        year_emotion_PMI[year] = {e: 0 for e in emotions} 
    
    for emot in emotions: 
        PMI_sum_emot = 0
        for lyric in lyrics:
            if lyric not in year_emotion_PMI_lyric[year][emot]: 
                continue
            PMI_sum_emot += year_emotion_PMI_lyric[year][emot][lyric]
        song_emotion_PMI[i][emot] = PMI_sum_emot
        #year_emotion_PMI[year][emot] += PMI_sum_emot
        max_PMI_emot[emot] = max(max_PMI_emot[emot], math.fabs(PMI_sum_emot))
    i += 1

print ("Song Polarities Calculated")

i = 0
for song in data:
    if len(song) < 3:
        continue
    year = song[0]
    for emot in emotions: 
        song_emotion_PMI[i][emot] /= max_PMI_emot[emot]
        year_emotion_PMI[year][emot] += song_emotion_PMI[i][emot]
    i += 1

print ("Song Polarities Normalized")

year_emot_score = {y : {e : year_emotion_PMI[y][e] / year_song_count[y] for e in emotions} for y in year_span}

print ("Year Polarities Calculated")

f = open('emotion_vector.txt', 'w')
i = 0

for song in data: 
    s = ""
    if len(song) < 3:
        continue
    year = song[0]
    genre = song[1]
    s += str(i) + " " + year + " " + genre
    for emot in emotions:  
        s += " " + str(song_emotion_PMI[i][emot])
    s += "\n"
    f.write(s)
    i += 1
f.close ()
    
print ("Wrote Song Emotion Vectors To File")
            

for emot in emotions: 
    pts = []    
    for year in year_span:
        pts.append(year_emot_score[year][emot])

    plt.plot(pts, "r-")
    plt.title(emot + " Emotion Vector Over Time")
    plt.ylim(-.2,.2) #Set yaxis range
    plt.gca().set_xticks(np.arange(len(year_span))) #label locations
    plt.gca().set_xticklabels(year_span) #label values
    plt.savefig("./Figures/" + emot + ".pdf")
    plt.close()

print ("Generated Graphs")





