#!/bin/python3
import os
import sys
import requests
import time
import traceback
import eyed3

client_id = 'Ud2k52mOdIEuIAUogCnrcqEgJOKrcIbv'
url = 'https://soundcloud.com/j4ix'
path = os.path.basename(url)
logfile = path + '.log'

os_illegal_chars = '\\/:*?"<>|'


def log(message):
    print(message)
    with open(logfile, 'a') as f:
        f.write(message + '\n')
    return None


def stacktrace():
    log(traceback.format_exc().rstrip('\n'))
    return sys.exit()


if not os.path.exists(path):
    os.mkdir(path)
open(logfile, 'w').close()
try:
    def get_data(url, *args):
        if not args:
            log(url)
        for i in range(4):
            try:
                r = requests.get(url)
                data = r
                if args:
                    data = data.json()['url']
            except KeyboardInterrupt:
                stacktrace()
            except Exception:
                if i == 3:
                    if args:
                        track_error()
                        return None
                    log('couldn\'t get data, quitting...')
                    stacktrace()
                if args:
                    log('[' + str(count) + '][' + str(i) +
                        ']something went wrong with "' + permalink + '", retrying...')
                else:
                    log('getting data failed, retrying...')
                continue
            return data

    def track_error(): return log(
        '[' + str(count) + '][' + str(i) + ']something went wrong with "' + permalink + '", skipping...')

    def get_meta():
        if track['artwork_url']:
            image_url = track['artwork_url'].replace('large', 't500x500')
        else:
            image_url = track['user']['avatar_url'].replace('large', 't500x500')
        image = get_data(image_url).content
        meta = eyed3.load(os.path.join(path, title))
        if not meta.tag:
            meta.initTag()
        meta.tag.version = (2, 3, 0)
        if '-' in track['title']:
            sep_title = track['title'].split('-', 1)
            sep_artist = sep_title[0].strip()
            sep_artist = sep_artist.split(')')[-1]
            sep_artist = sep_artist.split(']')[-1]
            meta.tag.artist = sep_artist.strip()
            meta.tag.title = sep_title[1].strip()
        else:
            meta.tag.artist = track['user']['username']
            meta.tag.title = track['title']
        if track['genre']:
            meta.tag.genre = track['genre']
        meta.tag.comments = u'penis '
        meta.tag.payment_url = track['permalink_url']
        meta.tag.release_date = track['display_date']
        meta.tag.images.set(3, image, 'image/jpeg')
        return meta.tag.save()

    api = 'https://api.soundcloud.com/resolve?url=' + url + '&client_id=' + client_id
    user_id = str(requests.get(api).json()['id'])
    # https://api-v2.soundcloud.com/users/210604704/likes?limit=1&client_id=Ud2k52mOdIEuIAUogCnrcqEgJOKrcIbv
    data = get_data('https://api-v2.soundcloud.com/users/' +
                    user_id + '/likes?limit=200&client_id=' + client_id).json()
    count = 0
    while True:
        for i in range(len(data['collection'])):
            count += 1
            if 'track' not in data['collection'][i]:
                log('[' + str(count) + '][' + str(i) + ']playlist, skipping...')
                continue
            track = data['collection'][i]['track']
            title = track['title'] + '.mp3'
            for x in os_illegal_chars:
                title = title.replace(x, '')
            title = title.strip()
            permalink = track['permalink_url']
            transcode = track['media']['transcodings']
            progressive = None
            for j in range(len(transcode)):
                if transcode[j]['format']['protocol'] == 'progressive':
                    progressive = j
                    break
            if not progressive:
                track_error()
                continue
            trackurl = track['media']['transcodings'][progressive]['url'] + \
                '?client_id=' + client_id
            trackurl = get_data(trackurl, True)
            log('[' + str(count) + '][' + str(i) + ']' +
                permalink + ' -> ' + trackurl)
            with requests.get(trackurl, stream=True) as r:
                with open(os.path.join(path, title), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=32*1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
            get_meta()
            stacktrace()
        if not data['next_href']:
            break
        data = get_data(data['next_href'] + '&client_id=' + client_id).json()
except (Exception, KeyboardInterrupt):
    stacktrace()
