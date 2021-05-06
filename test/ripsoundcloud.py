import os
import sys
from requests import get

url = "j4ix"
cid = "PgKFRG98vbasF0IWR0AuZ09A4TgDnwk1"
output = "."

illegal = '\\/:*?"<>|'


cid = "client_id=" + cid
api = "https://api-v2.soundcloud.com/resolve?url=https://soundcloud.com/" + \
    url + "&" + cid
uid = str(get(api).json()['id'])
likes = "https://api-v2.soundcloud.com/users/" + \
    uid + "/track_likes?limit=200&" + cid
r = get(likes).json()
data = []
while True:
    data.extend(r['collection'])
    if not r['next_href']:
        break
    r = get(r['next_href'] + "&" + cid).json()

if not os.path.exists(output):
    os.mkdir(output)


def get_prog():
    for i in range(len(transcodings)):
        if transcodings[i]['format']['protocol'] == 'progressive':
            return i
    return None


for x in reversed(data):
    if 'track' not in x:
        continue
    track = x['track']
    title = track['title']
    for i in illegal:
        title = title.replace(i, '')
    path = os.path.join(output, title + '.mp3')
    if os.path.isfile(path):
        continue
    transcodings = track['media']['transcodings']
    progressive = get_prog()
    if not progressive:
        continue
    print("downloading " + title + "...")
    with get(get(transcodings[progressive]['url'] + "?" + cid).json()['url'], stream=True) as r:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=32*1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
print("local up to date.")
