import csv
import collections

hiphop = []
genre = []
dates = []
songs_per_year = {}
text_file = open("Hip-Hop.txt", "w")

with open('../lyrics.csv', 'rb') as csv_lyrics:
	csv_reader = csv.reader(csv_lyrics, delimiter=',')

	for row in csv_reader:
		#Layout of csv: index,song,year,artist,genre,lyrics
		#So row[0] = index, row[1] = song ....
		curr_genre = row[4]
		song = row[1]
		curr_date = row[2]

		if curr_genre == "Hip-Hop":
			for thing in row:
				text_file.write(thing)
	

text_file.close()

