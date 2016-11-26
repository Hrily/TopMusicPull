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
# Variable number to get number of songs in the directory
TOP = 1000
# HTML Parser
html = HTMLParser.HTMLParser()
# Regex escape char replace
re_escape = r'\.|\$|\^|\{|\[|\(|\||\)|\]|\}|\*|\+|\?|\\|\'|\"'
# USAGE
# TODO: Think of good name
usage = 'USAGE : music_dl "PLAYLIST NAME" "FOLDER NAME" TOPNUMBER\n\nArguments:\n    "PLAYLIST NAME"\t: Name of the playlist (qoutes required!)\n    "FOLDER NAME"\t: Folder to download\n    TOPNUMBER\t\t: Integer, Number of videos to download starting from top\n    -h\t\t\t: Show this help'

# Extract query and folder name from command line
if len(sys.argv) == 1:
	print usage
	sys.exit()
elif len(sys.argv) == 2:
	if '-h' in sys.argv[1]:
		print usage
	else:
		print 'music_dl : no input folder name'
	sys.exit()
elif len(sys.argv) == 4:
	try:
		TOP = int(sys.argv[3])
	except:
		print 'music_dl : invalid input TOP number'
		sys.exit()
elif len(sys.argv) > 3:
	print usage
	sys.exit()

search_query = sys.argv[1].strip()
dir_name =  sys.argv[2].strip()
music_dir = music_dir + '"' + dir_name + '/"'

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
	sys.exit()

# Load link
link = match.group(1)
subprocess.call(wget + '"' + site + '/' + link + '"', shell = True)
f = open('result', 'r');
s = f.read()
subprocess.call('rm result', shell = True)
subprocess.call('rm log', shell = True)
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
	sys.exit()

# Create safe links and song names, Hash the links to song names
for i in range(len(links)):
	songs[i] = html.unescape(songs[i].strip()).replace('"', '').replace('/','').replace('$', 'S').replace('`', '');
	[title, artist, album] = get_metadata(songs[i])
	songs[i] = title
	if len(artist) > 0:
		songs[i] = title + ' - ' + artist
	songs[i] = songs[i].encode('utf-8')
	links[i] = html.unescape(links[i])

TOP = min(TOP, len(songs))

# Get old list and new list
proc = subprocess.Popen('ls '+ music_dir, stdout = subprocess.PIPE, shell = True)
oldlist = proc.stdout.read()
oldlist = oldlist.split('.mp3\n')
if '' in oldlist:
	oldlist.remove('')
old_songs = list(set(oldlist) - set(songs[0:TOP]))
new_songs = list(set(songs[0:TOP]) - set(oldlist))

# Remove Old songs not in list
if len(old_songs) > 0:
	print 'Found ' + str(len(old_songs)) + ' old song(s)'
	yn = raw_input('Remove Old songs not in list? (Y/n) ')
	if yn == 'y' or yn == 'Y':
		for song in old_songs:
			song = song.replace('/','').replace('$', 'S').replace('`', '');
			subprocess.Popen('rm '+ music_dir + '"' + song + '.mp3"', shell = True)
			print 'Removed  : ' + song

for i in range(TOP):
	song = songs[i]
	if song in new_songs:
		song = song.replace('/','').replace('$', 'S').replace('`', '');
		# Fetch new songs not in playlist
		print 'Fetching : ' + song
		proc = subprocess.Popen(ytdl + music_dir + '"' + song + '.%(ext)s" ' + site + links[i], stdout=subprocess.PIPE, shell = True)
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
	song = song.replace('/','').replace('$', 'S').replace('`', '');
	subprocess.Popen('mid3v2 ' + music_dir + '"' + song + '.mp3" -T "' + str(i+1) + '"', shell = True)

if len(new_songs) + len(old_songs) == 0:
	print 'Playlist up-to-date'
else:
	print 'Playlist updated'
