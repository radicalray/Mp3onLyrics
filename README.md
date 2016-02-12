# Mp3onLyrics
Download mp3 without knowing the name of the son - just by typing the lyrics or the youtube url

This program will also automatically search for the **Lyrics** of the song online then download the lyrics for the song and add then embed *Lyrics* to the *mp3* file via *eyed3* Tagger. All songs lyrics fetched in one go!


Just download the scipt and run my typing 


python music.py 

## Auto Tagger Module
Also includes an [auto-tagger](https://github.com/yask123/Auto-MP3-Lyrics-Tagger)

This will attempt to automatically tag the song with the proper artist/title from the title.

The following things takes place

* Reads the name of all *.mp3 files , stores the name in a list
* Iterating through each song name , send a get request at `Google.com` with the query `song_name Lyrics`
* Looks if the Lyrics Page (Metrolyrics or Azlyrics) is available
    * If present , scrape the lyrics
    * Uses Arc90 algorithm (behind readability) to pull out the lyrics from html pages to fight against anti-parsing techniques used on lyrics webpages. =)


Happy Downloading!



### Dependencies:

* `$ sudo pip install eyed3`
* libav ---- `brew install libav` 
* `$ sudo pip install BeautifulSoup4`

