#!/bin/python3

import os
import sys
import requests
import traceback
import eyed3


client_id = "Ud2k52mOdIEuIAUogCnrcqEgJOKrcIbv"
url = "https://soundcloud.com/j4ix"
genre_default = u"Dubstep"
track_numbers = True
cat_size = 24
path = os.path.basename(url)
logfile = path + ".log"
os_illegal_chars = '\\/:*?"<>|'

fuck_you = False


def log(message, status):
    if status == "inf":
        color = "\033[90m"
    elif status == "oof":
        color = "\033[91m"
    elif status == "dow":
        color = "\033[92m"
    elif status == "oop":
        color = "\033[93m"
    elif status == "api":
        color = "\033[94m"
    elif status == "cat":
        color = "\033[95m"
    elif status == "raw":
        color = "\033[95m"
    elif status == "img":
        color = "\033[96m"
    else:
        color = "\033[0m"
    if status == "usr" or status == "cat":
        message = "[" + status + "]" + message
    else:
        message = "[" + status + "][" + \
            str(count) + "][" + str(i) + "]" + message
    print(color + message + "\033[0m")
    with open(logfile, "a") as f:
        f.write(message + "\n")
    return None


def stacktrace():
    log(traceback.format_exc().rstrip("\n"), "cya")
    return sys.exit()


if not os.path.exists(path):
    os.mkdir(path)
open(logfile, "w").close()
try:
    def get_data(url, status):
        log(url, status)
        for j in range(4):
            try:
                r = requests.get(url)
                if status != "img":
                    r = r.json()
                    if fuck_you:
                        log(str(r), "raw")
            except KeyboardInterrupt:
                stacktrace()
            except Exception:
                if j == 3:
                    track_error(url)
                    return None
                log('something went wrong with "' +
                    url + '", retrying...', "oop")
                continue
            return r

    def track_error(url): return log(
        'something went wrong with "' + url + '", skipping...', "oof")

    def metadata():
        api = get_data(track["uri"] + "?client_id=" + client_id, "api")
        if api["artwork_url"]:
            image_url = api["artwork_url"].replace("large", "t500x500")
        else:
            image_url = api["user"]["avatar_url"].replace("large", "t500x500")
        image = get_data(image_url, "img").content
        meta = eyed3.load(target)
        meta.initTag((2, 3, 0))
        if "-" in api["title"]:
            artist_title = api["title"].split("-", 1)
            meta_artist = artist_title[0].strip()
            meta_title = artist_title[1].strip()
            meta_artist = meta_artist.split(")")[-1].strip()
            meta_artist = meta_artist.split("]")[-1].strip()
            meta.tag.artist = meta_artist
            meta.tag.title = meta_title
        else:
            meta.tag.artist = track["user"]["username"]
            meta.tag.title = track["title"]
        meta.tag.album = api["title"]
        if api["bpm"]:
            meta.tag.bpm = api["bpm"]
        if api["description"]:
            meta.tag.comments.set(api["description"])
        if api["genre"]:
            genre = api["genre"]
        else:
            genre = genre_default
        if genre:
            meta.tag.genre = genre
            meta.tag.setTextFrame("TCON", genre)
            log(genre, "inf")
        meta.tag.payment_url = api["permalink_url"]
        if api["release_year"]:
            meta.tag.recording_date = eyed3.core.Date(api["release_year"])
        else:
            meta.tag.recording_date = eyed3.core.Date(
                int(api["created_at"].split("/", 1)[0]))
        if track_numbers:
            meta.tag.track_num = count
        meta.tag.images.set(3, image, "image/jpeg", "Cover")
        return meta.tag.save()

    api = "https://api.soundcloud.com/resolve?url=" + url + "&client_id=" + client_id
    user_id = str(get_data(api, "usr")["id"])
    # https://api-v2.soundcloud.com/users/210604704/likes?limit=1&client_id=Ud2k52mOdIEuIAUogCnrcqEgJOKrcIbv
    api2 = get_data("https://api-v2.soundcloud.com/users/" + user_id +
                    "/likes?limit=" + str(cat_size) + "&client_id=" + client_id, "cat")

    count = 0
    while True:
        for i in range(len(api2["collection"])):
            progressive = False
            if "track" not in api2["collection"][i]:
                log("unsupported data type, skipping...", "inf")
                continue
            count += 1
            track = api2["collection"][i]["track"]
            target = track["title"]
            for x in os_illegal_chars:
                target = target.replace(x, "")
            target = os.path.join(path, target.strip() + ".mp3")
            if os.path.isfile(target):
                log("track fucking exists", "inf")
                continue
            transcode = track["media"]["transcodings"]
            for j in range(len(transcode)):
                if transcode[j]["format"]["protocol"] == "progressive":
                    progressive = j
                    break
            permalink = track["permalink_url"]
            if not progressive:
                track_error(permalink)
                continue
            url = track["media"]["transcodings"][progressive]["url"] + \
                "?client_id=" + client_id
            url = get_data(url, "api")["url"]
            log("[" + str(count) + "][" + str(i) + "]" +
                permalink + " -> " + url, "dow")
            with requests.get(url, stream=True) as r:
                with open(target, "wb") as f:
                    for chunk in r.iter_content(chunk_size=32*1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
            metadata()
            del(progressive)
        if not api2["next_href"]:
            break
        api2 = get_data(api2["next_href"] + "&client_id=" + client_id, "cat")
except (Exception, KeyboardInterrupt):
    stacktrace()
