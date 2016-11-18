#Import libraries
import re
import subprocess
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Fetches data drom this website
site = 'https://www.youtube.com'
#Version to wget to get 
wget = 'wget -q -o "log" -S '
#Downloads only the audio version of YouTube-dl
ytdl = 'youtube-dl --abort-on-error -x  --audio-format "mp3" -o "'
## Needs to be changed
music_dir = '/home/hrishi/Music/Billboard HOT 100/'
search_query = "Billboard HOT 100"
#Variable number to get number of songs in the directory
TOP = 30

def getFileName(f):
	''' Funcion to get shell safe file name '''
	# TODO: add more unsafe characters
	# NOTE: **Double Quoting** the characters also removes the unsafe character property  
	return f.replace(' ','\ ').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]').replace('&','\&')

print "Getting playlist..."


# Query search
search = 'results?search_query=' + search_query.replace(' ', '+')
subprocess.call(wget + site + '/' + search, shell=True)
f = open(search, 'r')
s = f.read();
subprocess.call('rm '+ search, shell=True)
atag = r'a href=.* class="yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link " .* title="Billboard HOT 100 .* href="/(.*)" class=" yt-uix-sessionlink      spf-link " .*View full playlist'
match = re.search(atag, s)

# Load link
link = match.group(1)
subprocess.call(wget + site + '/' + link, shell=True)
f = open(link, 'r');
s = f.read()
subprocess.call('rm '+ link, shell=True)
atag = r'a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link " .* href="(.*)" '
links = re.findall(atag, s)
atag = r'a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link " .*\n(.*)\n.*/a.*'
songs = re.findall(atag, s, re.MULTILINE);
hashlink = {}
for i in range(len(links)):
	songs[i] = html.unescape(songs[i].strip()).replace('"', '')
	links[i] = html.unescape(links[i])
	hashlink[songs[i]] = links[i]

# Get old list and new list
proc = subprocess.Popen('ls '+ music_dir.replace(' ','\ '), stdout = subprocess.PIPE, shell=True)
oldlist = proc.stdout.read()
oldlist = oldlist.split('.mp3\n')
oldlist.remove('')
old_songs = list(set(oldlist) - set(songs[0:TOP]))
new_songs = list(set(songs[0:TOP]) - set(oldlist))

# Remove Old songs not in list
for song in old_songs:
	subprocess.call('rm '+ music_dir.replace(' ','\ ') + getFileName(song) + '.*', shell=True)
	print "Removed  : " + song

# Fetch new songs not in list
for song in new_songs:
	print "Fetching : " + song
	proc = subprocess.Popen(ytdl + music_dir + song + '.%(ext)s" ' + site + hashlink[song], stdout=subprocess.PIPE, shell=True)
	#proc.wait()
	out = proc.communicate()[0]
	if "100%" in out:
		print "[DONE]"
	else:
		print "[Error]"

if len(new_songs) + len(old_songs) == 0:
	print "Playlist up-to-date"