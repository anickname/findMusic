import os
import mutagen.mp3
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class song():
    
    # tagExtensions = ('mp3', 'm4a', 'acc', 'wma')
    
    tagExtensions = ('mp3')

    def __init__(self):
        
        self.artist = "unknown"
        self.album = "unknown"
        self.songTitle = "unknown"
        self.bitrate = 0
        self.length = 0
        self.trackNumber = 0

        
    # def songObjFromFilename(songPath):
        # IMPLEMENT

    def songObjFromPlaylist(self, line):
        # tagList.append([x.rstrip() for x in line.split('\t')])

        self.artist = line["artist"]
        self.title = line["title"]
        self.album = line["album"]
        self.bitrate = line["bitrate"]
        self.length = line["length"]



    def songObjFromTags(self, songPath):
       
        try:
            s = MP3(songPath, ID3=EasyID3)

            self.artist = s['artist'][0] if 'artist' in s else u''    
            self.album = s['album'][0] if 'album' in s else u''
            self.title = s['title'][0] if 'title' in s else u''
            self.bitrate = unicode(s.info.bitrate / 1000)
            self.length = unicode(int(s.info.length))



            # return s
        
        #except Exception, exc:
        except(mutagen.mp3.error) as exc:
            print "Error! ", exc
            raise


    
     

    def isSupportedFileType(self, file):
        isSupported = False
        #Get file extension
        if (os.path.splitext(file)[1][1:].strip().lower() in self.tagExtensions):
           isSupported = True
        
        return isSupported


    def __hash__(self):
        return hash((self.artist, self.title, self.album)) 


    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


