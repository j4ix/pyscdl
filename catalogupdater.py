import os
import eyed3
from requests import get


url = "j4ix"
cid = "dmDh7QSlmGpzH9qQoH1YExYCGcyYeYYC"
output = "c:/users/j4ix/music"
do_meta = True
genre_default = "Dubstep"

illegal = '\\/:*?"<>|'




cid = "client_id=" + cid
api = "https://api-v2.soundcloud.com/resolve?url=https://soundcloud.com/" + \
    url + "&" + cid
uid = str(get(api).json()["id"])
likes = "https://api-v2.soundcloud.com/users/" + \
    uid + "/track_likes?limit=200&" + cid
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

if not os.path.exists(output):
    os.mkdir(output)


def get_prog():
    for i in range(len(transcodings)):
        if transcodings[i]["format"]["protocol"] == "progressive":
            return i
    return None


def fix(fix_title):
    for i in illegal:
        fix_title = fix_title.replace(i, "")
    path = os.path.join(output, fix_title + ".mp3")
    if os.path.isfile(path):
        print("REMOVING OLD FORMAT " + path)
        os.remove(path)
    path = os.path.join(output, fix_title.strip() + ".mp3")
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
    elif genre_default:
        genre = genre_default

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
    for i in illegal:
        target = target.replace(i, "")
    path = os.path.join(output, target + ".mp3")
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
