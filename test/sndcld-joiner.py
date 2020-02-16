import os
import requests

#startingValue = 0

print("initializing...")

client_id = "EIGGOBLgjWCWPGNJWglCXG8ifyl8WpCN"
url = "https://soundcloud.com/j4ix/sets/compiled-final"
api_resource = "http://api.soundcloud.com/resolve?url=" + url + "&client_id=" + client_id

r = requests.get(api_resource)
data = r.json()

playlistName = data["title"] + ""

if not os.path.exists("output"):
	os.mkdir("output")

BASE_PATH = os.path.abspath(os.path.dirname(__file__)) + "/" + "output"

print("starting download task for " + playlistName + "...")
#i = startingValue
for track in data["tracks"]:
	currentTrack = track["title"]

	print("fetching " + currentTrack + "...")
	streamLink = track["stream_url"] + "?client_id=" + client_id

	excluded_char = "\\/:*?\"<>|"
	for c in excluded_char:
		currentTrack = currentTrack.replace(c, "")

	#i += 1
	#currentTrack = str(i) + ". " + currentTrack
	currentTrack = currentTrack + ".mp3"
	path = os.path.join(BASE_PATH, currentTrack)

	data = requests.get(streamLink, stream=True)

	with open(path, "wb+") as f:
	    for chunk in data.iter_content(chunk_size=32*1024):
	        if chunk:
	            f.write(chunk)
	            f.flush()

print(playlistName + " finished.")
