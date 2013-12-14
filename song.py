import os
import mutagen.mp3
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class song(object):

    def __init__(self, tags):

        self.__artist = tags["artist"] if "artist" in tags else u'unknown'
        self.__title = tags["title"] if "title" in tags else u'unknown'
        self.__album = tags["album"] if "album" in tags else u'unknown'
        self.__bitrate = tags["bitrate"] if "bitrate" in tags else u'0'
        self.__length = tags["length"] if "length" in tags else u'0'

        
    @property
    def artist(self):
        return self.__artist

    @property
    def title(self):
        return self.__title

    @property
    def album(self):
        return self.__album

    @property
    def bitrate(self):
        return self.__bitrate

    @property
    def length(self):
        return self.__length

    @classmethod
    def songObjFromFile(cls, songPath):
        tags = {}
       
        try:
            s = MP3(songPath, ID3=EasyID3)

            tags["artist"] = s['artist'][0] if 'artist' in s else u''    
            tags["album"] = s['album'][0] if 'album' in s else u''
            tags["title"] = s['title'][0] if 'title' in s else u''
            tags["bitrate"] = unicode(
                    s.info.bitrate / 1000) if s.info.bitrate > 0 else u'0'
            tags["length"] = unicode(
                    int(s.info.length)) if s.info.length > 0 else u'0'

            songObj = cls(tags)
            return songObj

        #except Exception, exc:
        except(mutagen.mp3.error) as exc:
            print "Error! ", exc
            raise

     
    @staticmethod
    def isSupportedFileType(file):
        # tagExtensions = ('mp3', 'm4a', 'acc', 'wma')
        tagExtensions = ('mp3')

        isSupported = False
        #Get file extension
        if (os.path.splitext(file)[1][1:].strip().lower() in tagExtensions):
           isSupported = True
        
        return isSupported


    def __hash__(self):
        return hash((self.artist, self.title, self.album)) 


    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__

        return False

    def __repr__(self):
        return "%s({%s, %s, %s, %s, %s})" % (
                self.__class__,
                self.artist.encode('utf-8'),
                self.title.encode('utf-8'),
                self.album.encode('utf-8'),
                self.bitrate.encode('utf-8'),
                self.length.encode('utf-8')
                )


    def __str__(self):
        return "%s\t%s\t%s\t%s\t%s" % (
                self.__class__,
                self.artist.encode('utf-8'),
                self.title.encode('utf-8'),
                self.album.encode('utf-8'),
                self.bitrate.encode('utf-8'),
                self.length.encode('utf-8')
                )
