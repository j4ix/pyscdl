#!/bin/python3
import os
import sys
import requests
import traceback


client_id = 'Ud2k52mOdIEuIAUogCnrcqEgJOKrcIbv'
url = 'https://soundcloud.com/j4ix'
path = os.path.basename(url)
logfile = path + '.log'

os_illegal_chars = '\\/:*?"<>|'


def log(message):
    print(message)
    with open(logfile, 'a') as f:
        return f.write(message + '\n')


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
                data = r.json()
                if args:
                    data = data['url']
            except KeyboardInterrupt:
                stacktrace()
            except Exception:
                if i == 3:
                    if args:
                        track_error(args[0], args[1], args[2])
                        return
                    log('couldn\'t get data, quitting...')
                    stacktrace()
                if args:
                    log('[' + str(count) + '][' + str(i) +
                        ']something went wrong with "' + args[1] + '", retrying...')
                else:
                    log('getting data failed, retrying...')
                continue
            return data

    def track_error(count, i, permalink): return log(
        '[' + str(count) + '][' + str(i) + ']something went wrong with "' + permalink + '", skipping...')

    def main(count):
        for i in range(len(data['collection'])):
            if 'track' not in data['collection'][i]:
                continue
            count += 1
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
                track_error(count, i, permalink)
                continue
            trackurl = track['media']['transcodings'][progressive]['url'] + \
                '?client_id=' + client_id
            trackurl = get_data(trackurl, count, i, permalink)
            log('[' + str(count) + '][' + str(i) + ']' +
                permalink + ' -> ' + trackurl)
            with requests.get(trackurl, stream=True) as r:
                with open(os.path.join(path, title), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=32*1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
        return count

    api = 'https://api.soundcloud.com/resolve?url=' + url + '&client_id=' + client_id
    user_id = str(requests.get(api).json()['id'])
    # https://api-v2.soundcloud.com/users/210604704/likes?limit=24&client_id=Vu5tlmvC9eCLFZkxXG32N1yQMfDSAPAA
    data = get_data('https://api-v2.soundcloud.com/users/' +
                    user_id + '/likes?limit=200&client_id=' + client_id)
    count = 0
    while True:
        count = main(count)
        if not data['next_href']:
            break
        data = get_data(data['next_href'] + '&client_id=' + client_id)
except (Exception, KeyboardInterrupt):
    stacktrace()
