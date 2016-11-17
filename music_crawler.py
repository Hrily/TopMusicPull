import re
import subprocess

site = 'https://www.youtube.com'
wget = 'wget -S '

# Query search
search = 'results?search_query=billboard+top+100+this+week'
subprocess.call(wget+site+'/'+search, shell=True)
f = open(search, 'r')
s = f.read();
subprocess.call('rm '+search, shell=True)
atag = r'a href=.* class="yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link " .* title="Billboard HOT 100 .* href="/(.*)" class=" yt-uix-sessionlink      spf-link " .*View full playlist'
match = re.search(atag, s)

# Load link
link = match.group(1)
subprocess.call(wget+site+'/'+link, shell=True)
f = open(link, 'r');
s = f.read()
subprocess.call('rm '+link, shell=True)
atag = r'a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link " .* href="/(.*)" '
links = re.findall(atag, s)
print links[0]
atag = r'a class="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link " .*\n(.*)\n.*/a.*'
songs = re.findall(atag, s, re.MULTILINE);
playlist = [{}]*(len(links))
f = open("playlist", "w")
for i in range(len(links)):
	playlist[i]['index'] = i+1
	playlist[i]['song'] = songs[i].strip()
	playlist[i]['link'] = links[i]
	f.write(str(playlist[i])+'\n')

yt = 'youtube-dl '
yt1 = '"ytsearch:'

for i in range(10):
	subprocess.call(yt + site + '/' + links[i].replace('&amp;', '&'), shell=True)
