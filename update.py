update = __import__("run-search")

import sys

def do_update():
    if len(sys.argv) != 2:
        raise ValueError("update.py [bbs|bar] (bbs = bootlet beatsaver search, bar = beatmap author rankings")
    elif sys.argv[1] == "bbs":
        update.add_all_beatsaver_songs_to_database()
    elif sys.argv[1] == "bar":
        update.upload_all_author_stats_to_beatsaver()
        update.dodgy_writer()
    else:
        raise ValueError("valid args: 'bbs' or 'bar'")

if __name__ == "__main__":
    do_update()




