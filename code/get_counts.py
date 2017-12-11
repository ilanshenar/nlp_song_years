import csv
import collections
from string import punctuation

genre = []
dates = []
counts = {}
j = 0
with open('../lyrics.csv', 'rb') as csv_lyrics:
	csv_reader = csv.reader(csv_lyrics, delimiter=',')

	for row in csv_reader:
		#Layout of csv: index,song,year,artist,genre,lyrics
		#So row[0] = index, row[1] = song ....
		curr_genre = row[4]
		song = row[1]
		curr_date = row[2]
		lines = row[5].split("\n")
		
		for line in lines:
			words = line.split(" ")
			for word in words:
				if word == punctuation:
					continue
				if word == "":
					continue
				word = word.strip(punctuation).lower()
				if word not in counts:
					counts[word] = 1
				else:
					counts[word] += 1

counts = sorted(counts.items(), reverse=True, key=lambda x:x[1])

text_file = open("counts.txt", "w")

for word in counts:
	text_file.write(word[0] + ": " + str(word[1]) + "\n")

text_file.close()