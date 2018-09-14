import time
import datetime
import codecs
import requests
import json
from lxml import html
from requests.auth import HTTPBasicAuth
from BeatSaverSong import BeatSaverSong

api_url = "https://beatsaver.com/api/songs/detail/2435"

def parse_song(songid):
    songs = []
    api_url = "https://beatsaver.com/api/songs/detail/{}".format(songid)
    page = requests.get(api_url)
    jsonpage = page.json()
    song = jsonpage['song']
    for difficulty in song['difficulties']:
        id = song['id']
        key = song['key']
        name = song['name']
        description = song['description']
        uploader = song['uploader']
        uploaderid = song['uploaderId']
        songname = song['songName']
        songsubname = song['songSubName']
        author = song['authorName']
        bpm = song['bpm']
        downloadcount = song['downloadCount']
        finishedcount = song['playedCount']
        upvotes = song['upVotes']
        downvotes = song['downVotes']
        detailurl = song['linkUrl']
        downloadurl = song['downloadUrl']
        creationdate = song['createdAt']['date']
        coverurl = song['coverUrl']
        var = song['difficulties'][difficulty]
        difficulty = var['difficulty']
        audiopath = var['audioPath']
        jsonpath = var['jsonPath']
        songlength = var['stats']['time']
        if '8' in var['stats']['slashstat']:
            dotnotes = var['stats']['slashstat']['8']
        else:
            dotnotes = 0
        events = var['stats']['events']
        notes = var['stats']['notes']
        obstacles = var['stats']['obstacles']
        songs.append(BeatSaverSong(id,key,name,description,uploader,uploaderid,songname,songsubname,author,bpm,
                                   downloadcount,finishedcount,upvotes,downvotes,detailurl,downloadurl,creationdate,
                                   coverurl,difficulty,audiopath,jsonpath,songlength,dotnotes,events,notes,obstacles))
    return songs

def get_songs_starting_from(songnum):
    songs = []
    api_url = "https://beatsaver.com/api/songs/new/{}".format(songnum)

    page = requests.get(api_url)
    jsonpage = page.json()
    for song in jsonpage['songs']:
        for difficulty in song['difficulties']:
            id = song['id']
            key = song['key']
            name = song['name']
            description = song['description']
            uploader = song['uploader']
            uploaderid = song['uploaderId']
            songname = song['songName']
            songsubname = song['songSubName']
            author = song['authorName']
            bpm = song['bpm']
            downloadcount = song['downloadCount']
            finishedcount = song['playedCount']
            upvotes = song['upVotes']
            downvotes = song['downVotes']
            detailurl = song['linkUrl']
            downloadurl = song['downloadUrl']
            creationdate = song['createdAt']['date']
            coverurl = song['coverUrl']
            var = song['difficulties'][difficulty]
            difficulty = var['difficulty']
            audiopath = var['audioPath']
            jsonpath = var['jsonPath']
            time = var['stats']['time']
            if '8' in var['stats']['slashstat']:
                dotnotes = var['stats']['slashstat']['8']
            else:
                dotnotes = 0
            events = var['stats']['events']
            notes = var['stats']['notes']
            obstacles = var['stats']['obstacles']
            songs.append(BeatSaverSong(id,key,name,description,uploader,uploaderid,songname,songsubname,author,bpm,
                               downloadcount,finishedcount,upvotes,downvotes,detailurl,downloadurl,creationdate,
                               coverurl,difficulty,audiopath,jsonpath,time,dotnotes,events,notes,obstacles))




    return songs


def count_total_songs():
    api_url = "https://beatsaver.com/api/songs/new/"

    page = requests.get(api_url)
    jsonpage = page.json()
    total_songs = jsonpage['total']

    return total_songs



if __name__ == "__main__":
    song = parse_song(5684)
    print(song)
    songs = get_songs_starting_from(0)
    for song in songs:
        print(song.popularityrating)
    #print(get_song_info(15))