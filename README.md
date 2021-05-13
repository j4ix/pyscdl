# pyscdl
im pretty sure this isnt a good thing

this thing downloads mp3s from soundcloud with the most detailed metadata in the best way.

## extracting client id from soundcloud

in order to make this program work, you need to obtain a 32char string called a client-id from the exchange between your computer and soundcloud's servers. it's not that hard. in order to do this, open a new tab in your browser, hit `F12` and open the `Network` tab. then go to soundcloud's website and pay attention to the network log. you should see links in there that contain `api`. if not, filter by it. once you find one, click on it and copy the `client_id` value into the example batch file script provided. everytime the script fails to run, give it a new token by repeating this process start to finish.

### windows

you can download the exe and batch file and just edit the batch file and run that
the end

https://github.com/j4ix/pyscdl/releases

### anything else

install the latest python3 now
- if you're on mac go to https://www.python.org/downloads/
- if you're on linux do `sudo apt -y install python3`

once that's done install `eyed3` and `requests`

> pip install eyed3

> pip install requests

#### then

the main file is `catalogupdater.py`

edit and fill in the desired values including the client id obtained earlier. it will not work without the client id. if the client id goes stale get a new one.