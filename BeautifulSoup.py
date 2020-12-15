# 
# Project Partners: Hamza Asad, William Luna, Angel Ranjel
#     Student ID's: 45662901, 74953405, 44945284
#      UMich Email: asadh@umich.edu, lunawill@umich.edu, aranjel@umich.edu


import requests
import sqlite3
import math
import time
from bs4 import BeautifulSoup


rankList = []
songList = []
artistList = []
peakList = []
ratioList = []
weekYearVal = 52

# Web Scrape the billboard hot 100 with beautiful soup
source = requests.get("https://www.billboard.com/charts/hot-100")
soup = BeautifulSoup(source.content, 'html.parser')
container = soup.find_all('li', class_='chart-list__element display--flex')


for x in container:    # These are all in order from 1-100

    # 1st make a list contains the position on the billboard
    spanRank = x.find('span', class_='chart-element__rank__number')
    rankList.append(spanRank.text.strip())

    # 2nd make a list contains the song name      
    spanSong = x.find('span', class_='chart-element__information__song text--truncate color--primary')
    songList.append(spanSong.text.strip())

    # 3rd make a list that contains the artists
    spanArtist = x.find('span', class_='chart-element__information__artist text--truncate color--secondary')
    artistList.append(spanArtist.text.strip())

    # 4th make a list that contains the number of weeks on billboard top 100
    spanPeakTime = x.find('span', class_='chart-element__meta text--center color--secondary text--week')     
    peakList.append(spanPeakTime.text.strip())


# Calculation for a ratio of the number of weeks a song was on a billboard and put it in comparison
# with number of weeks in a year. Some songs will have more tham 52 which will result in ratio > 1
for y in range(len(peakList)):
    variable = float(peakList[y])
    yRatio = (variable/weekYearVal)
    yRatio = format(yRatio, ".3f")   
    ratioList.append(yRatio)


# The following inserts our data retrieved using beautiful soup into Hot100 database table

conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS Hot100 (position INTEGER, song TEXT, artist TEXT, numWeeks INTEGER, yearRatio INTEGER)')
cur.execute('SELECT * FROM Hot100')
rows = len(cur.fetchall())

# This conditional clause will only allow 25 data rows to be inserted in our database table everytime we run our program.
# Run the program 4 times to insert all 100 data rows into the database. 

if rows == 0:
    print('Inserting first 25 data rows')
    for x in range(0, 25):
        cur.execute('INSERT INTO Hot100 (position, song, artist, numWeeks, yearRatio) VALUES (?,?,?,?,?)', (rankList[x], songList[x], artistList[x], peakList[x], ratioList[x]))
elif rows == 25:
    print('Inserting second set of 25 data rows')
    for x in range(25, 50):
        cur.execute('INSERT INTO Hot100 (position, song, artist, numWeeks, yearRatio) VALUES (?,?,?,?,?)', (rankList[x], songList[x], artistList[x], peakList[x], ratioList[x]))
elif rows == 50:
    print('Inserting third set of 25 data rows')
    for x in range(50, 75):
        cur.execute('INSERT INTO Hot100 (position, song, artist, numWeeks, yearRatio) VALUES (?,?,?,?,?)', (rankList[x], songList[x], artistList[x], peakList[x], ratioList[x]))
elif rows == 75:
    print('Inserting last 25 data rows')
    for x in range(75, 100):
        cur.execute('INSERT INTO Hot100 (position, song, artist, numWeeks, yearRatio) VALUES (?,?,?,?,?)', (rankList[x], songList[x], artistList[x], peakList[x], ratioList[x]))
else:
    print('All data stored to database table.')
        
conn.commit()
cur.close()
