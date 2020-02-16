#!/bin/python3
import os
import sys
import requests
import time
import traceback


client_id = 'EIGGOBLgjWCWPGNJWglCXG8ifyl8WpCN'
url = 'https://soundcloud.com/j4ix'
logfile = os.path.join(os.path.dirname(__file__), os.path.basename(url))


def log(message):
    print(message)
    with open(logfile, 'a') as f:
        return f.write(message + '\n')


def stacktrace():
    log(traceback.format_exc().rstrip('\n'))
    return sys.exit()


open(logfile, 'w').close()
try:
    def get_data(url, *args):
        if not args:
            log(url)
        for i in range(4):
            try:
                r = requests.get(url)
                data = r.json()
            except KeyboardInterrupt:
                stacktrace()
            except Exception:
                if i == 3:
                    if args:
                        track_error()
                        return
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

    api = 'https://api.soundcloud.com/resolve?url=' + url + '&client_id=' + client_id
    user_id = str(requests.get(api).json()['id'])
    # https://api-v2.soundcloud.com/users/210604704/likes?limit=24&client_id=Vu5tlmvC9eCLFZkxXG32N1yQMfDSAPAA
    data = get_data('https://api-v2.soundcloud.com/users/' +
                    user_id + '/likes?limit=200&client_id=' + client_id)
    count = 0
    while True:
        for i in range(len(data['collection'])):
            if 'track' not in data['collection'][i]:
                continue
            count += 1
            track = data['collection'][i]['track']
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
            trackurl = get_data(trackurl, True)['url']
            log('[' + str(count) + '][' + str(i) + ']' +
                permalink + ' -> ' + trackurl)
            '''
            time.sleep(.5)
            '''
        if not data['next_href']:
            break
        data = get_data(data['next_href'] + '&client_id=' + client_id)
except (Exception, KeyboardInterrupt):
    stacktrace()
