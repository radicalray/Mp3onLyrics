#!/usr/bin/python

from __future__ import print_function
import os
from os import getcwd
from os.path import join

import re

from bs4 import BeautifulSoup
from urllib2 import urlparse
import glob

# Version compatiblity
import sys
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import quote_plus as qp
    raw_input = input
else:
    from urllib2 import urlopen
    from urllib import quote_plus as qp

from os.path import dirname
# calculated paths for django and the site
# used as starting points for various other paths
BASE_DIR = dirname(os.path.realpath(__file__))

def extract_videos(html):

    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/watch\?v=')
    found = soup.find_all('a', 'yt-uix-tile-link', href=pattern)
    return [(x.text.encode('utf-8'), x.get('href')) for x in found]


def list_movies(movies):
    for idx, (title, _) in enumerate(movies):
        yield '[{}] {}'.format(idx, title)


def search_videos(query):

    response = urlopen('https://www.youtube.com/results?search_query=' + query)
    return extract_videos(response.read())


def is_url(string):
    link = urlparse.urlparse(string)
    return bool(link.scheme)


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def download_from_url(url):
    print('Downloading', url)

    command_tokens = [
        'youtube-dl',
        '--output \'%(title)s.%(ext)s\'',
        # '--output \'' + join(getcwd(), 'download', '%(title)s.%(ext)s') + '\'',
        '--extract-audio',
        '--audio-format mp3',
        # '--audio-quality 0',
        '--format bestaudio',
        url]

    command = ' '.join(command_tokens)

    print('Downloading...')
    os.chdir(BASE_DIR)
    os.system(command)

    song_name= glob.glob("*.mp3")
    for name in song_name:
        try:

            # trim silences at the beginning and end of the song
            command_tokens = [
                'sox',
                 shellquote(name),
                 'temp.mp3',
                 'silence 1 0.1 1% reverse silence 1 0.1 1% reverse'
            ]
            command = ' '.join(command_tokens)

            print ('Trimming any silences...')
            os.system(command)
            print ('Done trimming, renaming...')
            os.system('mv temp.mp3 ' + shellquote(name))

        except Exception,e:
            print (e)
            traceback.print_exc()
            print ('An error occured for ', name)

    os.system('python ' + join(BASE_DIR, 'auto_lyrics_tagger.py -x'))

def main():

    search = ''
    while search.strip() == '':
        search = raw_input('Enter songname/lyrics/artist/url or other\n> ')

    print('Searching...')
    print (search)

    if is_url(search):
        print('You gave me an url')
        video_url = search
        download_from_url(video_url)
        print ('Finished downloading link!')
        return
        sys.exit()

    search = qp(search)
    available = search_videos(search)

    if not available:
        print('No results found matching your query.')
        sys.exit()

    print("Found:", '\n', '\n'.join(list_movies(available)))
    print ('-----------------------------------------------------------------')

    print('\n')

    choice = ''
    while choice.strip() == '':
        choice = raw_input('Pick one to download: ')

    title, video_link = available[int(choice)]

    # prompt = raw_input("Download (y/n)? ")
    # if prompt != "y":
    #     sys.exit()

    video_url = 'http://www.youtube.com' + video_link
    download_from_url(video_url)

if __name__ == '__main__':
    main()