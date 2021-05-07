#!/usr/bin/python3

import os
import sys
# import argparse    # believe me i did try it and i'm pretty sure i could if iw anted
import eyed3
from requests import get


def help():
    print(
        "usage: catalogupdater.exe [-h] <cid> <url> [output_dir] [default_genre] [do_meta]\n")
    print("required arguments:")
    print("  cid                client id")
    print("  url                soundcloud user by url\n")
    print("optional arguments:")
    print("  -h, --help         show this shit")
    print("  output_dir         output directory")
    print("  default_genre      default genre to use if none")
    print("  do_meta            compute metadata for downloaded tracks\n")
    print("examples:\n  catalogupdater.exe Mx2TehYCr804EIo6LQ7OARjZpWjMdVOx j4ix . Dubstep True")
    print("  catalogupdater.exe Mx2TehYCr804EIo6LQ7OARjZpWjMdVOx j4ix c:/users/j4ix/music \n\n\n")
    print("do what yu want")
    input()
    sys.exit()


""" parser = argparse.ArgumentParser()
parser.add_argument("cid", help="client id", required=False)
parser.add_argument("url", help="soundcloud user by url", required=False)
parser.add_argument("output_dir", help="output directory", required=False)
parser.add_argument("default_genre", help="default genre", required=False)
parser.add_argument("do_meta", help="compute song metadata", required=False)
args = parser.parse_args() """

if len(sys.argv) < 2:
    print("supposed to run this w tha batch bruhv")
    print("it won't do anything alone\n")
    help()
args = iter(sys.argv)
next(args)
for i in range(len(sys.argv) - 1):
    if i == 0:
        cid = next(args)
        #testmagic
        if len(cid) != 32:
            help()
    if i == 1:
        url = next(args)
    if i == 2:
        output_dir = next(args)
    if i == 3:
        default_genre = next(args)
    if i == 4:
        do_meta = next(args)
if len(sys.argv) < 6:
    print("enabling metadata processing")
    do_meta = True

illegal_os_chars = '\\/:*?"<>|'


cid = "client_id=" + cid
api = "https://api-v2.soundcloud.com/resolve?url=https://soundcloud.com/" + \
    url + "&" + cid
uid = str(get(api).json()["id"])
likes = "https://api-v2.soundcloud.com/users/" + \
    uid + "/track_likes?limit=100&" + cid
print("fetching likes list...")
r = get(likes).json()
data = []
while True:
    data.extend(r["collection"])
    if not r["next_href"]:
        break
    working = r["next_href"] + "&" + cid
    print(working)
    r = get(working).json()

if not output_dir:
    output_dir = "."
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


def get_prog():
    for i in range(len(transcodings)):
        if transcodings[i]["format"]["protocol"] == "progressive":
            return i
    return None


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


def metadata(artist, title):
    meta = eyed3.load(path).initTag((2, 3, 0))
    print("setting metadata for " + target)

    title = title.split('[')[0].strip()
    single = artist + " - " + title
    artist = artist.split(")")[-1].strip()
    artist = artist.split("]")[-1].strip()

    meta.artist = artist
    meta.title = title
    meta.album = single

    if track["description"]:
        meta.comments.set(track["description"])

    if track["genre"]:
        genre = track["genre"]
    elif default_genre:
        genre = default_genre
    else:
        genre = None

    if genre:
        meta.setTextFrame("TCON", genre)

    meta.payment_url = track["permalink_url"]

    meta.recording_date = eyed3.core.Date(
        int(track["created_at"].split("-", 1)[0]))

    if track["artwork_url"]:
        image_url = track["artwork_url"].replace("large", "t500x500")
    elif track["user"]["avatar_url"]:
        image_url = track["user"]["avatar_url"].replace("large", "t500x500")

    if image_url:
        image = get(image_url).content
        meta.images.set(3, image, "image/jpeg", "Cover")


# fix(artist + " - " + title)
    return meta.save()


print("downloading likes...")
for x in reversed(data):
    if "track" not in x:
        continue
    track = x["track"]
    if "-" in track["title"]:
        artist = track["title"].split('-', 1)[0].strip()
        title = track["title"].split('-', 1)[1].strip()
    else:
        artist = track["user"]["username"].strip()
        title = track["title"].strip()
    target = artist + " - " + title
    for i in illegal_os_chars:
        target = target.replace(i, "")
    path = os.path.join(output_dir, target + ".mp3")
    if os.path.isfile(path):
        # if do_meta:
        #metadata(artist, title)
        continue
    # fix(track["title"])
    transcodings = track["media"]["transcodings"]
    progressive = get_prog()
    if not progressive:
        continue
    print("downloading " + target + "...")
    with get(get(transcodings[progressive]["url"] + "?" + cid).json()["url"], stream=True) as r:
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=32*1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
    if do_meta:
        metadata(artist, title)


print("local up to date.")
