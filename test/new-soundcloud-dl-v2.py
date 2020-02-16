import os
import requests
import urllib.parse

client_id = 'pToAEVYicMm3OkPBnOlGCHfEBFrYx1fz'
profile = 'j4ix'

os_illegal_char = '\\/:*?"<>|'

api = 'https://api.soundcloud.com/resolve?url=https://soundcloud.com/' + profile + '&client_id=' + client_id
user = str(requests.get(api).json()['id'])
likes = 'https://api-v2.soundcloud.com/users/' + user + '/likes?limit=200&client_id=' + client_id
r = requests.get(likes).json()
open('output', 'w').close()
print(likes)
while True:
    for x in r['collection']:
        if 'track' in x:
            track = x['track']
            title = track['title']
            for x in os_illegal_char:
                title = title.replace(x, '')
            if 'media' in track:
                if track['media']['transcodings']:
                    url = requests.get(track['media']['transcodings'][1]['url'] + '?client_id=' + client_id).json()['url']
                    with open('output', 'a', encoding='utf-8', errors='replace') as f:
                        f.write(title + ' - ' + url + '\n')
        if 'playlist' in x:
            print('PLAYLIST REACHED')
            playlist = x['playlist']
            api = 'https://api-v2.soundcloud.com' + urllib.parse.urlparse(playlist['uri']).path + '?client_id=' + client_id
            collection = requests.get(api).json()
            for x in collection['tracks']:
                if 'title' in collection:
                    title = collection['title']
                    for x in os_illegal_char:
                        title = title.replace(x, '')
                    if 'media' in collection:
                        if collection['media']['transcodings']:
                            url = requests.get(x['media']['transcodings'][1]['url'] + '?client_id=' + client_id).json()['url']
                            with open('output', 'a', encoding='utf-8', errors='replace') as f:
                                f.write(title + ' - ' + url + '\n')
                    continue
                print('TRACK HAS NO INFO, DIGGING DEEPER')
                track_id = collection['id']
                api = 'https://api-v2.soundcloud.com/tracks/' + track_id + '?client_id=' + client_id
                subcollection = requests.get(api).json()
                if 'media' in subcollection:
                    if subcollection['media']['transcodings']:
                        url = requests.get(subcollection['media']['transcodings'][1]['url'] + '?client_id=' + client_id).json()['url']
                        with open('output', 'a', encoding='utf-8', errors='replace') as f:
                            f.write(url + '\n')
    if not r['next_href']:
        break
    print(r['next_href'] + '&client_id=' + client_id)
    r = requests.get(r['next_href'] + '&client_id=' + client_id).json()