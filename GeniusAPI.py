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
genius_key = "7_0HoQKH-fnnpXiZtMcafJH4q274mSGIxH_3cwgmDEgD-txE01axlkSjnggiyYGX"



# We imported the Spotipy library to help us use the Spotify API with a few Spotipy functions
# We contact the Spotify API using our client id's and secrets
# Returns a response from the Spotify API using the spotify_user_id and spotify_playlist_id  
def get_playlist_info():
    token = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret).get_access_token()
    sp = spotipy.Spotify(token)
    playlist = sp.user_playlist_tracks(spotify_user_id, spotify_playlist_id)
    return playlist
    


# This function uses the playlist json response and searches for track name and returns
# a list of track names
def get_track_names():    
    playlist = get_playlist_info()
    track_names = []
    
    for i in range(len(playlist['items'])):
        track_names.append(playlist['items'][i]['track']['name'])
    return track_names
    


# This function uses the playlist json response and searches for track artist names 
# returns a list of track artist names 
def get_track_artists():
    
    playlist = get_playlist_info()
    track_artists = []
    
    for i in range(len(playlist['items'])):
        track_artists.append(playlist['items'][i]['track']['artists'][0]['name'])
    return track_artists

    

# This function takes the url found in the response returned from the Genius API
# With the url the function scrapes the web for the song lyrics using Beautiful Soup 
def scrape_lyrics(url):
    song_url = url
    page = requests.get(song_url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics1 = html.find("div", class_="lyrics")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    return lyrics



# This function uses track names, artist names, and the Genius access token(key) to get 
# a response from Genius API. From the response we retrieved the URL to web scrape the Genius website
# and return the song lyrics. We used a series of conditonals and try/except clauses to catch any failed 
# web scrape attempts or a return of empty lyrics. Also included is a sleep timer.
def get_lyrics():

    track_names = get_track_names()
    track_artists = get_track_artists()
    song_lyrics = []

    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + genius_key}
    search_url = base_url + '/search'
    
    count = 0
    for i in range(len(track_names)):
        print("\n")
        print(f"Working on track {i+1}.")
        
        data = {'q': track_names[i] + ' ' + track_artists[i]}
        response = requests.get(search_url, data=data, headers=headers)
        json = response.json()
    
        remote_song_info = None
        for hit in json['response']['hits']:
            if track_artists[i].lower() in hit['result']['primary_artist']['name'].lower():
                remote_song_info = hit
                break
        
        if remote_song_info == None:
            lyrics = None
            print(f"Track {i+1} is not in the Genius database.")
            song_lyrics.append('N/A')
        else:
            url = remote_song_info['result']['url']
            lyrics = scrape_lyrics(url)
            if lyrics == None:
                print(f"Track {i+1} is not in the Genius database.")
            else:
                print(f"Retrieved track {i+1} lyrics!")
            song_lyrics.append(lyrics)
        count+=1
        
        if count % 25 == 0 and count < len(track_artists):
            print("Pausing for a bit...")
            time.sleep(5)
        elif count % 25 != 0 and count < len(track_artists):
            print('* * * * * * * * * * * * * * * * * * * * * *')
        else:
            print('All songs retrieved!')
    
    return song_lyrics


# This function selects all the lyrics data from the GeniusAPI database table and returns
# a tuple list of the lyrics. 
def get_lyrics_from_db():
    conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
    cur = conn.cursor()
    cur.execute("SELECT lyrics FROM GeniusAPI")
    lyrics_tuple_data = []
    for row in cur:
        lyrics_tuple_data.append(row)
    conn.commit()
    return lyrics_tuple_data


# This function takes the lyrics tuple data and iterates through the lyrics and 
# returns a list of the word count for each song in the database. 
def get_word_count(lyrics_tuple_data):
    word_counts = []
    for i in range(len(lyrics_tuple_data)):
        for line in lyrics_tuple_data[i]:
            line = line.split()
            count = len(line)
        word_counts.append(count)
    return word_counts


# This function takes the word_counts list returned from the lyrics data and calculates
# the average word count for all songs. 
def average_word_count(word_counts):
    sum = 0
    length = len(word_counts)
    for i in range(len(word_counts)):
        sum += word_counts[i]
    return round(sum/length)


# This function takes a track names list, a track artist list, and a song lyrics list to create
# the GeniusAPI database table
def setupSongTable(track_names, track_artists, song_lyrics):
        
    conn = sqlite3.connect('/Users/16169/Desktop/SI206/Final_Project/MusicStats.db')
    cur = conn.cursor()


    cur.execute('CREATE TABLE IF NOT EXISTS GeniusAPI (artist_id INTEGER PRIMARY KEY, song TEXT, artist TEXT, lyrics TEXT)')
    
    cur.execute("SELECT * FROM GeniusAPI")
    row_count = len(cur.fetchall())

    if row_count == 0:
        print('Inserting first 25 songs into database')
        for i in range(0,25):
            cur.execute('INSERT INTO GeniusAPI (artist_id, song, artist, lyrics) VALUES (?,?,?,?)', (i+1, track_names[i], track_artists[i], song_lyrics[i]))

    elif row_count == 25:
        print('Inserting second set of 25 songs into database')
        for i in range(25, 50):
            cur.execute('INSERT INTO GeniusAPI (artist_id, song, artist, lyrics) VALUES (?,?,?,?)', (i+1, track_names[i], track_artists[i], song_lyrics[i]))
    
    elif row_count == 50:
        print('Inserting third set of 25 songs into database')
        for i in range(50, 75):
            cur.execute('INSERT INTO GeniusAPI (artist_id, song, artist, lyrics) VALUES (?,?,?,?)', (i+1, track_names[i], track_artists[i], song_lyrics[i]))
    
    elif row_count == 75:
        print('Inserting last 25 songs into database')
        for i in range(75, 100):
            cur.execute('INSERT INTO GeniusAPI (artist_id, song, artist, lyrics) VALUES (?,?,?,?)', (i+1, track_names[i], track_artists[i], song_lyrics[i]))
    
    conn.commit()
    cur.close()


# Under main we call all our functions and write to a txt file a few of our calculations
def main():
    
    track_names=get_track_names()
    track_artists=get_track_artists()
    song_lyrics = get_lyrics()
    
    
    setupSongTable(track_names, track_artists, song_lyrics)
    
    lyrics_tuple_data = get_lyrics_from_db()
    word_counts = get_word_count(lyrics_tuple_data)
    average_words = average_word_count(word_counts)


    dir = os.path.dirname(__file__)
    out_file = open(os.path.join(dir, "calculations.txt"), "w", newline= '', encoding= 'utf-8')
    out_file.write('Average words of songs in playlist: ')
    out_file.write(str(average_words))
    out_file.write('\n')
    out_file.close()

# Standard call for main() function
if __name__ == '__main__':
    main()