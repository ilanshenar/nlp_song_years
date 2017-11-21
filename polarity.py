from __future__ import division
import operator 
import math
import collections
import csv
from string import punctuation

year_span = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]
year_songs = {x : [] for x in year_span}

max_num_songs = 1500

year_song_count = {x : 0 for x in year_span}
year_lyric_count = {x : {} for x in year_span}
year_lyric_count_angry = {x : {} for x in year_span}
year_lyric_count_disgust = {x : {} for x in year_span}
year_lyric_count_happy = {x : {} for x in year_span}
year_lyric_count_horror = {x : {} for x in year_span}
year_lyric_count_sad = {x : {} for x in year_span}
year_lyric_count_surprise = {x : {} for x in year_span}

angry_count = 1
disgust_count = 1
happy_count = 1
horror_count = 1
sad_count = 1
surprise_count = 1


angry_seeds = ["angry", "ugly", "mad", "anxious", "jaded", "ignorant", "frustrated", "jealous", "emotional", "insecure", "hungry", "confused", "cynical"]
disgust_seeds = ["disgust","scorn", "contempt", "disdain", "hatred", "guilt", "bitterness", "apathy", "anxiety", "fury", "vile", "anguish"]
happy_seeds = ["happy", "glad", "lucky", "alive", "good", "pleased", "satisfied", "thankful", "fine", "complete", "grateful", "content", "perfect"]
horror_seeds = ["horror", "chaos", "terror", "delusion", "gloom", "plague", "violence", "blackness", "bloodshed", "cruelty", "madness"]
sad_seeds = ["sad", "lonely", "miserable", "depressed", "boring", "tragic", "pathetic", "hopeless", "weird", "helpless"]
surprise_seeds = ["surprise", "warning", "shame", "mistake", "fool", "joke", "mystery", "thrill", "gift", "coincidence", "chance"]
#add words like "warn", "anger", "terrorize"????
with open('lyrics.csv', 'rb') as csv_lyrics:
    csv_reader = csv.reader(csv_lyrics, delimiter=',')

    for row in csv_reader:
        #Layout of csv: index,song,year,artist,genre,lyrics
        #So row[0] = index, row[1] = song ....
        curr_genre = row[4]
        curr_year = row[2]
        if curr_genre == "Hip-Hop" and curr_year in year_span:
            if year_song_count[curr_year] >= max_num_songs:
                continue
            year_song_count[curr_year] += 1
            
            lines = row[5].split("\n")
            lyrics = ""

            for line in lines:
                lyrics = lyrics + " " + line.lower()

            lyrics = lyrics.translate(None, punctuation)
            lyric_list = lyrics.split(" ")
            
            
            
            is_angry = False
            if any(x in lyric_list for x in angry_seeds):
                angry_count += 1
                is_angry = True
            is_disgust = False
            if any(x in lyric_list for x in disgust_seeds):
                disgust_count += 1
                is_disgust = True
            is_happy = False
            if any(x in lyric_list for x in happy_seeds):
                happy_count += 1
                is_happy = True
            is_horror = False
            if any(x in lyric_list for x in horror_seeds):
                horror_count += 1
                is_horror = True
            is_sad = False
            if any(x in lyric_list for x in sad_seeds):
                sad_count += 1
                is_sad = True
            is_surprise = False
            if any(x in lyric_list for x in surprise_seeds):
                surprise_count += 1
                is_surprise = True
            
            for lyric in lyric_list:
                if lyric == punctuation:
                    lyric_list.remove(lyric)
                    continue
                if lyric == "":
                    lyric_list.remove(lyric)
                    continue
                    
                if lyric not in year_lyric_count[curr_year]:
                    year_lyric_count[curr_year][lyric] = 1
                    year_lyric_count_angry[curr_year][lyric] = 1
                    #year_lyric_count_disgust[curr_year][lyric] = 1
                    #year_lyric_count_happy[curr_year][lyric] = 1
                    #year_lyric_count_horror[curr_year][lyric] = 1
                    #year_lyric_count_sad[curr_year][lyric] = 1
                    #year_lyric_count_surprise[curr_year][lyric] = 1
                    
                else:
                    year_lyric_count[curr_year][lyric] += 1
                if is_angry:
                    year_lyric_count_angry[curr_year][lyric] += 1
            #   if is_disgust:
            #       year_lyric_count_disgust[curr_year][lyric] += 1
            #	if is_happy:
            #       year_lyric_count_happy[curr_year][lyric] += 1
            #	if is_horror:
            #       year_lyric_count_horror[curr_year][lyric] += 1
            #   if is_sad:
            #       year_lyric_count_sad[curr_year][lyric] += 1
            #	if is_surprise:
            #       year_lyric_count_surprise[curr_year][lyric] += 1
            year_songs[curr_year].append(lyric_list)

year_PMI_lyric_angry = {x : {} for x in year_span}
year_PMI_song_angry = {x : [] for x in year_span}
            
for year in year_span:
    for lyric, var in year_lyric_count[year].items():
        co_occ = year_lyric_count_angry[year][lyric] / max_num_songs
        occ_x = year_lyric_count[year][lyric] / max_num_songs
        occ_y = angry_count / max_num_songs
        year_PMI_lyric_angry[year][lyric] = co_occ / (occ_x * occ_y)
        
    for lyric_list in year_songs[year]:
        PMI_sum_angry = 0
        for lyric in lyric_list: 
            PMI_sum_angry += year_PMI_lyric_angry[year][lyric]
        year_PMI_song_angry[year].append(PMI_sum_angry)

year_Anger_score = {x : sum(year_PMI_song_angry[x]) / len(year_PMI_song_angry[x]) for x in year_span}
print (year_Anger_score)
            
            
            
            
            
"""
sorted_anger = sorted(anger.items(), reverse=True, key=lambda x:x[1])
#sorted_disgust = sorted(disgust.items(), reverse=True, key=lambda x:x[1])
#sorted_happy = sorted(happy.items(), reverse=True, key=lambda x:x[1])
#sorted_horror = sorted(horror.items(), reverse=True, key=lambda x:x[1])
#sorted_sad = sorted(sad.items(), reverse=True, key=lambda x:x[1])
#sorted_surprise = sorted(surprise.items(), reverse=True, key=lambda x:x[1])

def write_out(name, emotion):
	name = "polarity_counts/" + name + ".txt"
	text_file = open(name, "w")

	for word in emotion:
		text_file.write(word[0] + "," + str(word[1]) + "," + str(counts[word[0]]) + "," + str(angry_count) +  "\n")

	text_file.close()

write_out("anger_2016", sorted_anger)
#write_out("disgust", sorted_disgust)
#write_out("happy", sorted_happy)
#write_out("horror", sorted_horror)
#write_out("sad", sorted_sad)
#write_out("surprise", sorted_surprise)
"""