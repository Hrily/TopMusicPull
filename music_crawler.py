import re
import subprocess

site = 'https://www.youtube.com'
wget = 'wget -q -o "log" -S '
ytdl = 'youtube-dl -x  --audio-format "mp3" -o "'
music_dir = '/home/hrishi/Music/Billboard HOT 100/'
search_query = "Billboard HOT 100"
TOP = 3

def getFileName(f):
	''' Funcion to get shell safe file name '''
	# TODO: add more unsafe characters
	return f.replace(' ','\ ').replace('(',"\(").replace(')','\)').replace('[','\[').replace(']','\]')

print "Getting playlist..."

# Query search
search = 'results?search_query=' + search_query.replace(' ', '+')
subprocess.call(wget+site+'/'+search, shell=True)
f = open(search, 'r')
s = f.read();
subprocess.call('rm '+ search, shell=True)
atag = r'a href=.* class="yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link " .* title="Billboard HOT 100 .* href="/(.*)" class=" yt-uix-sessionlink      spf-link " .*View full playlist'
match = re.search(atag, s)

# Load link
link = match.group(1)
subprocess.call(wget+site+'/'+link, shell=True)
f = open(link, 'r');
s = f.read()
subprocess.call('rm '+ link, shell=True)
atag = r'a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link " .* href="(.*)" '
links = re.findall(atag, s)
atag = r'a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link " .*\n(.*)\n.*/a.*'
songs = re.findall(atag, s, re.MULTILINE);
hashlink = {}
for i in range(len(links)):
	songs[i] = songs[i].strip();	
	hashlink[songs[i]] = links[i]

# Get old list and new list
proc = subprocess.Popen('ls '+music_dir.replace(' ','\ '), stdout=subprocess.PIPE, shell=True)
oldlist = proc.stdout.read()
oldlist = oldlist.split('.mp3\n')
oldlist.remove('')
old_songs = list(set(oldlist) - set(songs[0:TOP]))
new_songs = list(set(songs[0:TOP]) - set(oldlist))

# Remove Old songs not in list
for song in old_songs:
	subprocess.call('rm '+ music_dir.replace(' ','\ ') + getFileName(song) + '.*', shell=True)
	print "Removed : " + song

# Fetch new songs not in list
for song in new_songs:
	print "Fetching : " + song
	proc = subprocess.Popen(ytdl + music_dir + song + '.%(ext)s" ' + site + hashlink[song].replace('&amp;', '&'), stdout=subprocess.PIPE, shell=True)
	out = proc.communicate()[0]
	if "100%" in out:
		print "[DONE]"
	else:
		print "[Error]"

if len(new_songs)+len(old_songs) == 0:
	print "Playlist up-to-date"