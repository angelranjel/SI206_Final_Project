# 
# Project Partners: Hamza Asad, William Luna, Angel Ranjel
#     Student ID's: 45662901, 74953405, 44945284
#      UMich Email: asadh@umich.edu, lunawill@umich.edu, aranjel@umich.edu


import sys
import spotipy
import spotipy.util as util
import requests
import unittest
import sqlite3
import json
import os
import time
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup


# Global Constants that allow us to access the Spotify and Genius API's
# To get the following variable you must sign up and register online to access the Spotify and Genius API
spotify_client_id = "384531d1c01d4ea4b4fc9cbdb54740a5"
spotify_client_secret = "93c9145bd0b94192ae5edf5c2f9127b3"
spotify_user_id = "spotify:user:hairyorange"
spotify_playlist_id = "spotify:playlist:1EVE9kOZ2i4171hNdvWVhU"


# We imported the Spotipy library to help us use the Spotify API with a few Spotipy functions
# We contact the Spotify API using our client id's and secrets
# Returns a response from the Spotify API using the spotify_user_id and spotify_playlist_id
def get_playlist_info():
    token = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret).get_access_token()
    sp = spotipy.Spotify(token)
    playlist = sp.user_playlist_tracks(spotify_user_id, spotify_playlist_id)
    return playlist


# Function condenses all our data requests from the Spotify API json response into one function
# We access track name, track album type, track popularity, track duration in ms,
# and track artist names into their appropriate lists and return them.
def get_track_information():    
    
    playlist = get_playlist_info()
    track_names = []
    trackType = []
    trackPopularity = []
    trackDuration = []
    track_artists = []
    
    for i in range(len(playlist['items'])):    
        
        # What we did was go through the json response element and pulled relevent consistent data
        track_names.append(playlist['items'][i]['track']['name'])
        trackType.append(playlist['items'][i]['track']['album']['album_type'])
        trackPopularity.append(playlist['items'][i]['track']['popularity'])
        trackDuration.append(playlist['items'][i]['track']['duration_ms'])
        track_artists.append(playlist['items'][i]['track']['artists'][0]['name'])

    return track_names, trackType, trackPopularity, trackDuration, track_artists


# This function selects the popularity data from the SpotifySongAPI table 
# and returns the popularity tuple list. It then calculates the popularity average 
# by converting the tuple data into integers. Returns the popularity average
def get_pop_from_database():

    conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM SpotifySongAPI")
    rows = len(cur.fetchall())

    if rows == 100:

        cur.execute("SELECT popularity FROM SpotifySongAPI")
        results = cur.fetchall()

        pVal=[]
        for x in results:
            x = str(x)
            x = x.strip("(),")
            x = int(x)
            pVal.append(x)  # Converted to integer for calculations

        pSum = 0
        for i in range(len(pVal)):
            pSum+=pVal[i]
            
        pAve = pSum/(len(pVal))
        return(pAve)

    else:
        pass


# This function selects the song duration data from the SpotifySongAPI table 
# and returns the duration tuple list. It then calculates the duration average 
# by converting the tuple data into integers. Returns the duration average
def get_time_from_database():

    conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM SpotifySongAPI")
    rows = len(cur.fetchall())

    if rows == 100:

        cur.execute("SELECT duration FROM SpotifySongAPI")
        results = cur.fetchall()

        dVal=[]
        for x in results:
            x = str(x)
            x = x.strip("(),")
            x = int(x)
            dVal.append(x)  # Converted to integer for calculations

        dSum = 0
        for i in range(len(dVal)):
            dSum+=dVal[i]

        dAve = (dSum/(len(dVal)))/1000
        return format(dAve, ".3f")

    else:
        pass
        

# This function uses the playlist json response and searches for track artist names 
# returns a list of track artist names
def get_track_artists():
    
    playlist = get_playlist_info()
    track_artists = []
    
    for i in range(len(playlist['items'])):
        track_artists.append(playlist['items'][i]['track']['artists'][0]['name'])
    return track_artists


# This function takes a track artist list to create the SpotifyAPI database table
# The database table houses each unique artist with a unique artist key
def setUpArtistTable(track_artists):
    
    artistList = []

    for i in range(len(track_artists)):
        if track_artists[i] not in artistList:
            artistList.append(track_artists[i])
        
    conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS SpotifyAPI (artist_id INTEGER, artist TEXT)')
    
    cur.execute('SELECT * FROM SpotifyAPI')
    rows = len(cur.fetchall())
    
    # This conditional clause will only allow 25 data rows or until data rows are exhausted to be inserted 
    # in our database table everytime we run the program.
    if rows == 0:
        for x in range(0, 25):
            cur.execute('INSERT INTO SpotifyAPI (artist_id, artist) VALUES (?,?)', (x+1, artistList[x]))
    
    elif rows == 25:
        for x in range(25, 50):
            cur.execute('INSERT INTO SpotifyAPI (artist_id, artist) VALUES (?,?)', (x+1, artistList[x]))
    
    elif rows == 50:
        for x in range(50, len(artistList)):
            cur.execute('INSERT INTO SpotifyAPI (artist_id, artist) VALUES (?,?)', (x+1, artistList[x]))
    
    conn.commit()
    cur.close()


# This function takes a track names list, a track artist list, and track album type, 
# a track duration list, and a track popularity list to create the SpotifySongAPI database table
# The function also selects artist and artist id data from SpotifyAPI table so we can insert 
# into the new SpotifySongAPI table. Also contains a sleep timer.
def setUpInfoTable(track_names, trackType, trackPopularity, trackDuration, track_artists):

    conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
    cur = conn.cursor()

    cur.execute("SELECT artist, artist_id FROM SpotifyAPI")
    dbTuple = cur.fetchall()
    dbTuple = dict(dbTuple)

    
    cur.execute('CREATE TABLE IF NOT EXISTS SpotifySongAPI (song TEXT, artist_id INTEGER, type TEXT, popularity INTEGER, duration INTEGER)')
    cur.execute('SELECT * FROM SpotifySongAPI')
    rows = len(cur.fetchall())
    
    # This conditional clause will only allow 25 data rows to be inserted in our database table everytime we run our program.
    # Run the program 4 times to insert all 100 data rows into the database.
    if rows == 0:
        print('Inserting first 25 data rows')
        for x in range(0, 25):
            cur.execute('INSERT INTO SpotifySongAPI (song, artist_id, type, popularity, duration) VALUES (?,?,?,?,?)', (track_names[x], dbTuple[track_artists[x]], trackType[x], trackPopularity[x], trackDuration[x]))
            time.sleep(.05)
            print(f'Working on dataset {x+1}')
    elif rows == 25:
        print('Inserting second 25 data rows')
        for x in range(25, 50):
            cur.execute('INSERT INTO SpotifySongAPI (song, artist_id, type, popularity, duration) VALUES (?,?,?,?,?)', (track_names[x], dbTuple[track_artists[x]], trackType[x], trackPopularity[x], trackDuration[x]))
            time.sleep(.05)
            print(f'Working on dataset {x+1}')    
    elif rows == 50:
        print('Inserting third 25 data rows')
        for x in range(50, 75):
            cur.execute('INSERT INTO SpotifySongAPI (song, artist_id, type, popularity, duration) VALUES (?,?,?,?,?)', (track_names[x], dbTuple[track_artists[x]], trackType[x], trackPopularity[x], trackDuration[x]))
            time.sleep(.05)
            print(f'Working on dataset {x+1}')
    elif rows == 75:
        print('Inserting last 25 data rows')
        for x in range(75, 100):
            cur.execute('INSERT INTO SpotifySongAPI (song, artist_id, type, popularity, duration) VALUES (?,?,?,?,?)', (track_names[x], dbTuple[track_artists[x]], trackType[x], trackPopularity[x], trackDuration[x]))
            time.sleep(.05)
            print(f'Working on dataset {x+1}')
    else:
        print('All data stored to database table.')
        print('Calculations file now available.')
        cur.close()


    conn.commit()

    # cur.close()


# This function uses the SELECT and JOIN methods to combine data tables to select
# popularity data that is greater than or equal to 70 and that is longer than 10000 ms in duration.
def joining_tables():

    conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
    cur = conn.cursor()
    

    cur.execute("SELECT * FROM SpotifySongAPI")
    rows = len(cur.fetchall())
    if rows == 100:


        cur.execute(f"SELECT SpotifySongAPI.popularity FROM SpotifySongAPI JOIN SpotifyAPI ON SpotifySongAPI.artist_id = SpotifyAPI.artist_id WHERE SpotifySongAPI.popularity >= 70 AND SpotifySongAPI.duration >= 10000")
        
        results = cur.fetchall()

        upVal=[]
        for x in results:
            x = str(x)
            x = x.strip("(),")
            x = int(x)
            upVal.append(x)  # Converted to integer for calculations

        upSum = 0
        for i in range(len(upVal)):
            upSum+=upVal[i]

        upPopAve = (upSum/(len(upVal)))

        return upPopAve
    else:
        pass



# This function takes in data calculations: duration average, popularity average, average popularity of the 
# most popular songs and writes the calculations to a txt file.
def writeCalculation(dAve, pAve, upPopAve):
    conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
    cur = conn.cursor()
    

    cur.execute("SELECT * FROM SpotifySongAPI")
    rows = len(cur.fetchall())
    if rows == 100:
        out_file = open("calculations.txt", "a", newline= '', encoding= 'utf-8')
        out_file.write('Average popularity for songs in playlist: ')
        out_file.write(str(pAve))
        out_file.write('\n')
        out_file.write('Average time for songs in playlist: ')
        out_file.write(str(dAve))
        out_file.write(' seconds!')
        out_file.write('\n')
        out_file.write('Average Popularity of the most popular songs above 70: ')
        out_file.write(str(upPopAve))

        out_file.close()
        


# Under main we call all our functions and write to a txt file a few of our calculations
def main():
    
    track_names, trackType, trackPopularity, trackDuration, track_artists = get_track_information()
    track_artists=get_track_artists()
    setUpArtistTable(track_artists)
    setUpInfoTable(track_names, trackType, trackPopularity, trackDuration, track_artists)
    upPopAve = joining_tables()
    pAve = get_pop_from_database()
    dAve = get_time_from_database()
    writeCalculation(dAve, pAve, upPopAve)

if __name__ == '__main__':
    main()