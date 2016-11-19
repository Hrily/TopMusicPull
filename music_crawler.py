#Import libraries
import re
import subprocess
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Fetches data drom this website
site = 'https://www.youtube.com'
# Version to wget to get 
wget = 'wget -q -O "result" -o "log" -S '
# Downloads only the audio version of YouTube-dl
ytdl = 'youtube-dl --abort-on-error -x --audio-format "mp3" -o '
# Needs to be changed
music_dir = '~/Music/'
dir_name = ''
search_query = ''
music_dir = music_dir + '/"' + dir_name + '/"'
# Variable number to get number of songs in the directory
TOP = 10
# HTML Parser
html = HTMLParser.HTMLParser()
# Regex escape char replace
re_escape = r'\.|\$|\^|\{|\[|\(|\||\)|\]|\}|\*|\+|\?|\\|\'|\"'
# USAGE
usage = 'USAGE : python music_crawler.py "PLAYLIST NAME" "FOLDER NAME"'

# Extract query and folder name from command line
# TODO: update USAGE
if len(sys.argv) == 1:
	print usage
	exit()
elif len(sys.argv) == 2:
	print 'music_crawler : no input folder name'
	exit()
elif len(sys.argv) > 3:
	print usage
	exit()

search_query = sys.argv[1]
dir_name =  sys.argv[2]

def get_metadata(song):
	''' Function to get Artist,Title from song name '''
	extra = re.compile(r'((\[|\()official(\]|\))*)|((\[|\()*lyric(s)*(\]|\))*)|((\[|\()*video(\]|\)))|((\[|\()*music video(\]|\)))|((\[|\()*audio(\]|\))*)', re.I)
	ft = re.compile(r'(\()*(ft.|feat.)(.*)(\))*', re.I)
	album_re = re.compile(r'\(from (.*)\)', re.I)
	title = ''
	artist = ''
	album = ''
	song = re.sub(extra, '', song)
	# Extract Album name
	album_g = re.search(album_re, song)
	song = re.sub(album_re, '', song)
	if album_g is not None:
		album = album_g.group(1)
	# Extract Title and Artist	
	meta = re.split(r'(:|-|~)', song)
	title = meta[0]
	if len(meta) >= 3:
		title = meta[2]
		artist = meta[0]
		# Extract ft
		feature = re.search(ft, title)
		title = re.sub(ft, '', title)
		if feature is not None:
			artist = artist.strip() + ' ' + feature.group()
	return [title.strip(), artist.strip(), album.strip()]

print 'Getting playlist...'

# Make the music directory if not available
subprocess.Popen('mkdir -p ' + music_dir, shell = True)

# Query search
search = 'results?search_query=' + search_query.replace(' ', '+')
subprocess.call(wget + '"' +  site + '/' + search + '"', shell = True)
f = open('result', 'r')
s = f.read();
s = html.unescape(s)
atag = r'a href=.* class="yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link " .* title="' + re.sub(re_escape, '.', search_query) + '.* href="/(.*)" class=" yt-uix-sessionlink      spf-link " .*View full playlist'
match = re.search(atag, s)

if match is None or match.group(1) is None:
	print '[Error] : Cannot find the playlist - ' + search_query
	exit()

# Load link
link = match.group(1)
subprocess.call(wget + '"' + site + '/' + link + '"', shell = True)
f = open('result', 'r');
s = f.read()
#subprocess.call('rm result', shell = True)
atag = r'a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link " .* href="(.*)" '
links = re.findall(atag, s)
atag = r'a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link " .*\n(.*)\n.*/a.*'
songs = re.findall(atag, s, re.MULTILINE);
atag = r'h1 class="pl-header-title".*\n(.*)\n.*/h1'
playlist_title = re.search(atag, s, re.MULTILINE)

# Confirm playlist from user
print 'Playlist Title : \033[1m' + html.unescape(playlist_title.group(1)).strip() + '\033[0m'
print 'Top videos :'
for i in range(min(3, len(songs))):
	print '\t'+songs[i]
yn = raw_input('Download? (Y/n) ')
if yn != 'y' and yn != 'Y':
	exit()

# Create safe links and song names, Hash the links to song names
hashlink = {}
for i in range(len(links)):
	songs[i] = html.unescape(songs[i].strip()).replace('"', '')
	links[i] = html.unescape(links[i])
	hashlink[songs[i]] = links[i]

# Get old list and new list
proc = subprocess.Popen('ls '+ music_dir, stdout = subprocess.PIPE, shell = True)
oldlist = proc.stdout.read()
oldlist = oldlist.split('.mp3\n')
if '' in oldlist:
	oldlist.remove('')
old_songs = list(set(oldlist) - set(songs[0:TOP]))
new_songs = list(set(songs[0:TOP]) - set(oldlist))

# Sometime double check is required
for song in new_songs:
	if song in oldlist:
		new_songs.remove(song)
		old_songs.remove(song)

# Remove Old songs not in list
print 'Found ' + str(len(old_songs)) + ' old song(s)'
yn = raw_input('Remove Old songs not in list? (Y/n) ')
if yn == 'y' or yn == 'Y':
	for song in old_songs:
		subprocess.Popen('rm '+ music_dir + '"' + song + '.mp3"', shell = True)
		print 'Removed  : ' + song

for i in range(TOP):
	song = songs[i]
	if song in new_songs:
		# Fetch new songs not in playlist
		print 'Fetching : ' + song
		proc = subprocess.Popen(ytdl + music_dir + '"' + song + '.%(ext)s" ' + site + hashlink[song], stdout=subprocess.PIPE, shell = True)
		#proc.wait()
		out = proc.communicate()[0]
		if "100%" in out:
			print '[DONE]\nSetting id3 tags'
			[title, artist, album] = get_metadata(song)
			# Set metadata of the song
			subprocess.Popen('mid3v2 ' + music_dir + '"' + song + '.mp3" -t "' + title + '" -a "' + artist + '"', shell = True)
			print '[DONE]'
		else:
			print 'youtube-dl : [Error]'
			continue
	# Update song rank
	subprocess.Popen('mid3v2 ' + music_dir + '"' + song + '.mp3" -T "' + str(i+1) + '"', shell = True)

if len(new_songs) + len(old_songs) == 0:
	print 'Playlist up-to-date'
else:
	print 'Playlist updated'