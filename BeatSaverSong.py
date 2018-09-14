import time
import datetime
import codecs
import requests
import json
from lxml import html
from requests.auth import HTTPBasicAuth
from datetime import datetime




class BeatSaverSong():


    def __init__(self, id, key, name, description, uploader, uploaderid, songname, songsubname, author, bpm,
                 downloadcount, finishedcount, upvotes, downvotes, detailurl, downloadurl,creationdate, coverurl, difficulty,
                 audiopath, jsonpath, time, dotnotes, events, notes, obstacles):
        self.id = id
        self.key = key
        self.name = name
        self.description = description
        self.uploader = uploader
        self.uploaderid = uploaderid
        self.songname = songname
        self.songsubname = songsubname,
        self.author = author
        self.bpm = bpm
        self.downloadcount = downloadcount
        self.finishedcount = finishedcount
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.detailurl = detailurl
        self.downloadurl = downloadurl
        self.coverurl = coverurl
        self.difficulty = difficulty
        self.audiopath = audiopath
        self.jsonpath = jsonpath
        self.time = time
        self.dotnotes = dotnotes
        self.events = events
        self.notes = notes
        self.creationdate = creationdate
        self.obstacles = obstacles
        self.daysold = self.age_in_days()
        self.songlength = self.song_length()
        self.difficultyrating = self.difficulty_rating()
        self.popularityrating = self.popularity_rating()
        self.popularityratingovertime = self.populatiry_rating_over_time()
        self.completionratio = self.completion_ratio()

    def song_length(self):
        return self.time / self.bpm * 60

    def difficulty_rating(self):
        totalnotes = self.notes - self.dotnotes + (self.dotnotes/4)

        difficultyrating = round(totalnotes / self.songlength,2)

        return difficultyrating

    def age_in_days(self):
        created = self.creationdate.split(' ')[0]
        now = datetime.now()
        created = datetime.strptime(created, '%Y-%m-%d')

        age = now - created

        days = age.days
        if days == 0:
            return 1
        else:
            return days

    def populatiry_rating_over_time(self):
        upvotes = 5 + self.upvotes
        downvotes = 5 + self.downvotes
        rating = upvotes / downvotes

        return rating / self.daysold * 10

    def popularity_rating(self):
        upvotes = 5 + self.upvotes
        downvotes = 5 + self.downvotes
        rating = upvotes / downvotes

        return rating

    def completion_ratio(self):
        return self.finishedcount / self.downloadcount


