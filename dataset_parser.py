import csv
import collections

hiphop = []
genre = []
dates = []
songs_per_year = {}

with open('lyrics.csv', 'rb') as csv_lyrics:
	csv_reader = csv.reader(csv_lyrics, delimiter=',')

	for row in csv_reader:
		#Layout of csv: index,song,year,artist,genre,lyrics
		#So row[0] = index, row[1] = song ....
		curr_genre = row[4]
		song = row[1]
		curr_date = row[2]

		if curr_genre == "Hip-Hop":
			hiphop.append(song)
			if curr_date not in dates:
				dates.append(curr_date)
			if curr_date in songs_per_year:
				songs_per_year[curr_date] += 1
			else:
				songs_per_year[curr_date] = 1


print(len(hiphop))
dates.sort(key=int)
print(dates)
songs_per_year = collections.OrderedDict(sorted(songs_per_year.items()))
for year in songs_per_year:
	print(str(year) + ": " + str(songs_per_year[year]))
