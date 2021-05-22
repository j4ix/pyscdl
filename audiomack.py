#!/usr/bin/python3

import os
import sys
import eyed3
from datetime import date
from urllib.parse import quote_plus
from requests import get


oauth_nonce = quote_plus("uescauxPYwsAYX4qrjs2YFe8LjbJKGMX")
oauth_timestamp = 1621719971
oauth_signature = quote_plus("vB/GsHnAmM0tzn6xeLSVa4HulWU=")
url = "https://audiomack.com/andrekrynski/playlist/juice-wrld"
output_dir = "c:/users/j4ix/documents/testdirectory"
default_genre = ""
do_meta = True

illegal_os_chars = '\\/:*?"<>|'


url = url.split("/")
if url[4] != "playlist":
    sys.exit()
print(url)

api = "https://api.audiomack.com/v1/playlist/" + url[3] + "/" + url[5] + "?oauth_consumer_key=audiomack-js&oauth_nonce=" + \
    oauth_nonce + "&oauth_signature_method=HMAC-SHA1&oauth_timestamp=" + \
    str(oauth_timestamp) + "&oauth_version=1.0&oauth_signature=" + oauth_signature
print(get(api).json())

likes = "https://api-v2.soundcloud.com/users/" + "/track_likes?limit=100&"
print("fetching likes list...")
r = get(api).json()


if not output_dir:
    output_dir = "."
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


"""
def get_prog():
    for i in range(len(transcodings)):
        if transcodings[i]["format"]["protocol"] == "progressive":
            return i
    return None
"""


"""
def fix(fix_title):
    for i in illegal_os_chars:
        fix_title = fix_title.replace(i, "")
    path = os.path.join(output_dir, fix_title + ".mp3")
    if os.path.isfile(path):
        print("REMOVING OLD FORMAT " + path)
        os.remove(path)
    path = os.path.join(output_dir, fix_title.strip() + ".mp3")
    if os.path.isfile(path):
        print("REMOVING OLD FORMAT " + path)
        os.remove(path)
"""


def metadata():
    meta = eyed3.load(path).initTag((2, 3, 0))
    print("setting metadata for " + target)

    
    if not track["artist"]:
        if "-" in track["title"]:
            artist = track["title"].split('-', 1)[0].strip()
            title = track["title"].split('-', 1)[1].strip()
        else:
            artist = track["uploader"]["name"].strip()
            title = track["title"].strip()
        title = track["title"].split('[')[0].strip()
        artist = artist.split(")")[-1].strip()
        artist = artist.split("]")[-1].strip()
    else:
        title = track["title"]
        artist = track["artist"]

    meta.artist = track["artist"]
    meta.title = title
    meta.album = artist + ' - ' + title


    if track["genre"]:
        genre = track["genre"]
    elif default_genre:
        genre = default_genre
    else:
        genre = None

    if genre:
        meta.setTextFrame("TCON", genre)

    meta.payment_url = track["links"]["self"]

    meta.recording_date = eyed3.core.Date(
        int(str(date.fromtimestamp(int(track["released"]))).split("-")[0]))

    if track["image"]:
        image_url = track["image"]
    elif track["uploader"]["image"]:
        image_url = track["uploader"]["image"]

    if image_url:
        image = get(image_url).content
        meta.images.set(3, image, "image/jpeg", "Cover")


# fix(artist + " - " + title)
    return meta.save()


print("downloading likes...")
for x in reversed(r['results']['tracks']):
    track = x
    """
    if not x["artist"]:
        if "-" in track["title"]:
            artist = track["title"].split('-', 1)[0].strip()
            title = track["title"].split('-', 1)[1].strip()
        else:
            artist = track["user"]["username"].strip()
            title = track["title"].strip()
        target = artist + " - " + title
    """
    target = track["streaming_url"].split("/")[5].split("?")[0]

    pass
    for i in illegal_os_chars:
        target = target.replace(i, "")
    if '.mp3' not in target:
        target += '.mp3'
    path = os.path.join(output_dir, target)
    if os.path.isfile(path):
        # if do_meta:
        #metadata(artist, title)
        continue
    # fix(track["title"])
    print("downloading " + target + "...")
    with get(track["streaming_url"], stream=True) as r:
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=32*1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
    if do_meta:
        metadata()


print("local up to date.")
