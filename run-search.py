import requests
import simplejson as json
from BeatSaverSong import BeatSaverSong
from psycopg2 import connect

api_url = "https://beatsaver.com/api/songs/detail/2435"


with open("settings.json", 'r') as file:
    settings = json.load(file)
    username = settings['username']
    password = settings['password']
    database = settings['database']
    db_endpoint = settings['db_endpoint']
    db_port = settings['db_port']

def debugging(event,context):
    #print("{},{},{},{},{}".format(database,username,password,db_endpoint,db_port))
    print("Event: {}".format(event))
    print("Context: {}".format(context))
    return {
        "statusCode": 200,
        "body": json.dumps({"event": str(event)})
    }

def search_for_song_with_params(event, context):
    conn = connect(dbname=database, user=username, host=db_endpoint,port=db_port, password=password)
    cursor = conn.cursor()
    wherestatement = ""
    orderby = ""
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        queryparams = event['queryStringParameters']
        queries = []

        if 'songname' in queryparams:
            queries.append("lower(songname) like lower('%" + queryparams['songname'] + "%')")

        if 'songsubname' in queryparams:
            queries.append("lower(songsubname) like lower('%" + queryparams['songsubname'] + "%')")

        if 'author' in queryparams:
            queries.append("lower(author) like lower('%" + queryparams['author'] + "%')")

        if 'difficulty' in queryparams:
            queries.append("lower(difficulty) = lower('" + queryparams['difficulty'] +"')")

        if 'mindifficultyrating' in queryparams:
            queries.append("difficultyrating >= {}".format(queryparams['mindifficultyrating']))

        if 'maxdifficultyrating' in queryparams:
            queries.append("difficultyrating <= {}".format(queryparams['maxdifficultyrating']))

        if 'minpopularityrating' in queryparams:
            queries.append("popularityrating >= {}".format(queryparams['minpopularityrating']))

        if 'maxpopularityrating' in queryparams:
            queries.append("popularityrating <= {}".format(queryparams['maxpopularityrating']))

        if 'orderby' in queryparams and 'order' in queryparams:
            orderby = "order by {} {}".format(queryparams['orderby'],queryparams['order'])

        if 'daysold' in queryparams:
            queries.append("daysold <= {}".format(queryparams['daysold']))

        if 'completed' in queryparams:
            if queryparams['completed'] == 'yes':
                queries.append("completionratio > 0")


        wherestatement = "where " + " AND ".join(queries)


    selectstatement = """
            select songname,author,coverurl, difficulty, difficultyrating, downloadurl,popularityrating,songsubname,upvotes,downvotes,completionratio,daysold,id from songs
            {}
            {}
        """.format(wherestatement,orderby)
    cursor.execute(selectstatement)
    data = cursor.fetchall()
    body = []
    for song in data:
        body.append({
            "songname" : song[0],
            "author" : song[1],
            "coverurl" : song[2],
            "difficulty" : song[3],
            "difficultyrating" : song[4],
            "downloadurl" : song[5],
            "popularityrating" : song[6],
            "songsubname" : song[7],
            "upvotes" : song[8],
            "downvotes" : song[9],
            "completionratio" : song[10],
            "daysold" : song[11],
            "id" : song[12]
        })
    print(body)
    return {
        "statusCode": 200,
        "headers" : {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": json.dumps(body)
    }


def get_my_songs(event, context):
    conn = connect(dbname=database, user=username, host=db_endpoint,port=db_port, password=password)
    cursor = conn.cursor()
    selectstatement = """
        select songname,author,coverurl, difficulty, difficultyrating, downloadurl,popularityratingovertime,songsubname,upvotes,downvotes,completionratio,daysold from songs
        where author = 'Zeekin'
        order by difficultyrating desc
    """
    cursor.execute(selectstatement)
    data = cursor.fetchall()
    body = []
    for song in data:
        body.append({
            "songname" : song[0],
            "author" : song[1],
            "coverurl" : song[2],
            "difficulty" : song[3],
            "difficultyrating" : song[4],
            "downloadurl" : song[5],
            "popularityratingovertime" : song[6],
            "songsubname" : song[7],
            "upvotes" : song[8],
            "downvotes" : song[9],
            "completionratio" : song[10],
            "daysold" : song[11]
        })
    return {
        "statusCode": 200,
        "headers" : {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": json.dumps(body)
    }

def add_all_beatsaver_songs_to_database():
    totalcount = count_total_beatsaver_songs()
    counter = 0
    while(counter < totalcount):
        print("Beginning Adding songs {} to {}...".format(counter,counter+20))
        songs = get_songs_starting_from(counter)
        update_and_add_songs_to_database(songs)
        print("Finished Adding songs {} to {}.".format(counter,counter+20))
        #beatsaver api gives 20 songs at a time
        counter+=20

def update_and_add_songs_to_database(zsongs):

    simpleinsert = """
        INSERT INTO  "public"."songs" ("id", "difficulty") values (1337, 'leet')
    """

    conn = connect(dbname=database, user=username, host=db_endpoint,port=db_port, password=password)
    cursor = conn.cursor()
    for zsong in zsongs:
        replacestatement = 'INSERT INTO "public"."songs" ("id", "songkey", "name", "description", "uploader", "uploaderid", ' \
                           '"songname", "songsubname", "author", "bpm", "downloadcount", "finishedcount", "upvotes", ' \
                           '"downvotes", "detailurl", "downloadurl", "coverurl", "difficulty", "audiopath", "jsonpath", ' \
                           '"songtime", "dotnotes", "events", "notes", "creationdate", "obstacles", "daysold", ' \
                           '"songlength", "difficultyrating", "popularityrating", "popularityratingovertime", ' \
                           '"completionratio")' \
                            ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
                           '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
                           'ON CONFLICT (ID, Difficulty) DO UPDATE ' \
                           'SET ID = %s, SongKey = %s, Name = %s, Description = %s, Uploader = %s, UploaderID = %s,' \
                           'SongName = %s, SongSubName = %s, Author = %s, BPM = %s, DownloadCount = %s,' \
                           'FinishedCount = %s, UpVotes = %s, DownVotes = %s, DetailURL = %s, DownloadURL = %s,' \
                           'CoverURL = %s, Difficulty = %s, AudioPath = %s, JSONPath = %s, SongTime = %s,' \
                           'DotNotes = %s, Events = %s, Notes = %s, CreationDate = %s, Obstacles = %s,' \
                           'DaysOld = %s, SongLength = %s, DifficultyRating = %s, PopularityRating = %s,' \
                           'PopularityRatingOverTime = %s, CompletionRatio = %s'

        cursor.execute(replacestatement, (zsong.id, zsong.key, zsong.name, zsong.description, zsong.uploader, zsong.uploaderid,
                                         zsong.name, zsong.songsubname, zsong.author, zsong.bpm, zsong.downloadcount,
                                         zsong.finishedcount,  zsong.upvotes, zsong.downvotes, zsong.detailurl, zsong.downloadurl,
                                         zsong.coverurl, zsong.difficulty, zsong.audiopath, zsong.jsonpath, zsong.time,
                                         zsong.dotnotes, zsong.events, zsong.notes, zsong.creationdate, zsong.obstacles,
                                         zsong.daysold, zsong.songlength, zsong.difficultyrating, zsong.popularityrating,
                                         zsong.popularityratingovertime, zsong.completionratio,
                                          zsong.id, zsong.key, zsong.name, zsong.description, zsong.uploader, zsong.uploaderid,
                                          zsong.name, zsong.songsubname, zsong.author, zsong.bpm, zsong.downloadcount,
                                          zsong.finishedcount,  zsong.upvotes, zsong.downvotes, zsong.detailurl, zsong.downloadurl,
                                          zsong.coverurl, zsong.difficulty, zsong.audiopath, zsong.jsonpath, zsong.time,
                                          zsong.dotnotes, zsong.events, zsong.notes, zsong.creationdate, zsong.obstacles,
                                          zsong.daysold, zsong.songlength, zsong.difficultyrating, zsong.popularityrating,
                                          zsong.popularityratingovertime, zsong.completionratio))

    conn.commit()

    return "heh"

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
            songsubname = str(song['songSubName'])
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
            if isinstance(var['stats']['slashstat'],dict) and '8' in var['stats']['slashstat']:
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


def count_total_beatsaver_songs():
    api_url = "https://beatsaver.com/api/songs/new/"

    page = requests.get(api_url)
    jsonpage = page.json()
    total_songs = jsonpage['total']

    return total_songs



if __name__ == "__main__":
    #get_my_songs("a","b")
    #search_for_song_with_params({
    #    "queryStringParameters" : {
    #        "songname" : "RED",
    #        "orderby" : "difficultyrating",
    #        "order" : "desc",
    #        "maxdifficultyrating": 15,
    #        "mindifficultyrating": 2
    #    }
    #},"a")
    add_all_beatsaver_songs_to_database()