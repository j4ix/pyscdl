import os
import time
import requests
import urllib.parse

client_id = 'Vu5tlmvC9eCLFZkxXG32N1yQMfDSAPAA'
profile = 'j4ix'
path = 'soundcloud'

os_illegal_char = '\\/:*?"<>|'

print('initializing...')
if not os.path.exists(path):
	os.mkdir(path)
api = 'https://api.soundcloud.com/resolve?url=https://soundcloud.com/' + profile + '&client_id=' + client_id
user_id = str(requests.get(api).json()['id'])
likes = 'https://api-v2.soundcloud.com/users/' + user_id + '/likes?limit=200&client_id=' + client_id
r = requests.get(likes)
data = r.json()
print(user_id)
print(likes)
while True:
    for x in data['collection']:
        if 'track' in x:
            track = x['track']
            title = track['title']
            filename = title + '.mp3'
            for x in os_illegal_char:
                filename = filename.replace(x, '')
            if os.path.isfile(os.path.join(path, filename)):
                print(title + ' exists, skipping')
                continue
            if track['media']['transcodings']:
                print('processing ' + title + '...')
                url = requests.get(track['media']['transcodings'][1]['url'] + '?client_id=' + client_id).json()
        time.sleep(.5)
    if not r['next_href']:
        break
    next_href = data['next_href'] + '&client_id=' + client_id
    print(next_href)
    r = requests.get(next_href)
    data = r.json()
