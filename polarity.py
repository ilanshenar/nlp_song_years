from __future__ import division
import operator 
import math
import collections
import csv
from string import punctuation

counts = {}
anger = {}
disgust = {}
happy = {}
horror = {}
sad = {}
surprise = {}

i = 0
lyric_list = []
angry_seeds = ["angry", "ugly", "mad", "anxious", "jaded", "ignorant", "frustrated", "jealous", "emotional", "insecure", "hungry", "confused", "cynical"]
disgust_seeds = ["disgust","scorn", "contempt", "disdain", "hatred", "guilt", "bitterness", "apathy", "anxiety", "fury", "vile", "anguish"]
happy_seeds = ["happy", "glad", "lucky", "alive", "good", "pleased", "satisfied", "thankful", "fine", "complete", "grateful", "content", "perfect"]
horror_seeds = ["horror", "chaos", "terror", "delusion", "gloom", "plague", "violence", "blackness", "bloodshed", "cruelty", "madness"]
sad_seeds = ["sad", "lonely", "miserable", "depressed", "boring", "tragic", "pathetic", "hopeless", "weird", "helpless"]
surprise_seeds = ["surprise", "warning", "shame", "mistake", "fool", "joke", "mystery", "thrill", "gift", "coincidence", "chance"]
#add words like "warn", "anger", "terrorize"????
with open('../lyrics.csv', 'rb') as csv_lyrics:
	csv_reader = csv.reader(csv_lyrics, delimiter=',')

	for row in csv_reader:
		if i > 1500:
			break
		#Layout of csv: index,song,year,artist,genre,lyrics
		#So row[0] = index, row[1] = song ....
		curr_genre = row[4]
		curr_year = row[2]
		if curr_genre == "Hip-Hop" and curr_year == "2016":
			i += 1
			lines = row[5].split("\n")
			lyrics = ""
			
			for line in lines:
				lyrics = lyrics + " " + line.lower()

			lyrics = lyrics.translate(None, punctuation)
			lyric_list = lyrics.split(" ")
			
			for lyric in lyric_list:
				if lyric == punctuation:
					continue
				if lyric == "":
					continue
				if lyric not in counts:
					counts[lyric] = 1
					anger[lyric] = 1
					disgust[lyric] = 1
					happy[lyric] = 1
					horror[lyric] = 1
					sad[lyric] = 1
					surprise[lyric] = 1
				else:
					counts[lyric] += 1
				if any(angry_word in lyric_list for angry_word in angry_seeds):
					anger[lyric] += 1
			#	if any(disgust_word in lyric_list for disgust_word in disgust_seeds):
			#		disgust[lyric] += 1
			#	if any(happy_word in lyric_list for happy_word in happy_seeds):
			#		happy[lyric] += 1
			#	if any(horror_word in lyric_list for horror_word in horror_seeds):
			#		horror[lyric] += 1
			#	if any(sad_word in lyric_list for sad_word in sad_seeds):
			#		sad[lyric] += 1
			#	if any(surprise_word in lyric_list for surprise_word in surprise_seeds):
			#		surprise[lyric] += 1


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
		text_file.write(word[0] + ": " + str(word[1]) + "\n")

	text_file.close()

write_out("anger_2016", sorted_anger)
#write_out("disgust", sorted_disgust)
#write_out("happy", sorted_happy)
#write_out("horror", sorted_horror)
#write_out("sad", sorted_sad)
#write_out("surprise", sorted_surprise)