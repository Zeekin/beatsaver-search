import datetime
from datetime import datetime

class AuthorApprovalRating():

    def __init__(self, authorname, upvotes, downvotes, newestmapage, mapcount):
        self.authorname = authorname
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.approvalrating = self.approval_rating()
        self.newestmapage = newestmapage
        self.mapcount = mapcount
        self.avgmapvotes = self.avg_map_votes()

    def approval_rating(self):
        return (self.upvotes + 5) / (self.upvotes + self.downvotes + 10)

    def avg_map_votes(self):
        return (self.upvotes - self.downvotes) / self.mapcount




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
        self.songsubname = songsubname
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
        self.completionratio = self.completion_ratio()
        self.daysold = self.age_in_days()
        self.songlength = self.song_length()
        self.difficultyrating = self.difficulty_rating()
        self.popularityrating = self.popularity_rating()
        self.popularityratingovertime = self.popularitry_rating_over_time()


    def song_length(self):
        if self.bpm == 0:
            return 0
        else:
            return self.time / self.bpm * 60

    def difficulty_rating(self):
        if self.songlength == 0:
            return 0

        totalnotes = self.notes - self.dotnotes

        difficultyrating = round(totalnotes / self.songlength * (1-(self.completionratio * 0.33)),2)
        if difficultyrating < 0.5 and difficultyrating != 0:
            return 0.5
        else:
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

    def popularitry_rating_over_time(self):
        upvotes = 5 + self.upvotes
        downvotes = 5 + self.downvotes
        rating = upvotes / downvotes

        return rating

    def popularity_rating(self):
        upvotes = 5 + self.upvotes
        downvotes = 5 + self.downvotes
        rating = upvotes / (upvotes + downvotes) * 100

        return rating

    def completion_ratio(self):
        if self.downloadcount == 0:
            return 0
        else:
            ratio = self.finishedcount / self.downloadcount
            if ratio > 1:
                return 1
            else:
                return ratio



