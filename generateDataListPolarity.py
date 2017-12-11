import csv
from string import punctuation

max_num_songs = 10000
year_span = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]
genres = ["Hip-Hop", "Pop", "Rock", "Country", "R&B"]

year_song_count = {g : {x : 0 for x in year_span} for g in genres}
total_year_songs = {x : 0 for x in year_span}
total = 0

data = []
minlen = 25

min_length = 1500

f = open('data.txt', 'w')

with open('lyrics.csv', 'rb') as csv_lyrics:
    csv_reader = csv.reader(csv_lyrics, delimiter=',')
    for row in csv_reader:
        #Layout of csv: index,song,year,artist,genre,lyrics
        #So row[0] = index, row[1] = song ....
        curr_genre = row[4]
        curr_year = row[2]
        
        if curr_year in year_span:
            total_year_songs[curr_year] += 1
        
        if curr_genre in genres and curr_year in year_span:
            if year_song_count[curr_genre][curr_year] >= max_num_songs:
                continue
            
           
            
            lines = row[5].split("\n")
            
            if len(lines) < minlen:
                continue
            total += 1    
                
                
            year_song_count[curr_genre][curr_year] += 1
            
            lyrics = ""

            for line in lines:
                lyrics = lyrics + " " + line.lower()

            lyrics = lyrics.translate(None, punctuation)
            lyric_list = lyrics.split(" ")
            for lyric in lyric_list:
                
                if lyric == punctuation:
                    lyric_list.remove(lyric)
                    continue
                if lyric == "":
                    lyric_list.remove(lyric)
                    continue
            
            if len(lyric_list) < min_length:
                min_length = len(lyric_list)
            
            lyrics = ""
            for lyric in lyric_list:
                lyrics += lyric + " "
            f.write(curr_year + "," + curr_genre + "," + lyrics + "\n")
f.close()
print(total)
print(total_year_songs)
print("")
print(year_song_count)

            
        
            
    
    