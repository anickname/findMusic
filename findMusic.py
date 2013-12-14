import os
import errno
import sys
import codecs
import shutil

from song import song

import mutagen.mp3





def main():
    #program variables
    playlistFile = "/home/nick/tmp/music/playlist.txt"
    rootdir = "/home/nick/tmp/music/"
    copyDestination = "/home/nick/tmp/music_found/"
    log_foundSongs = copyDestination + "songs_found.txt"
    log_songsNotFound = copyDestination + "songs_notfound.txt"

    #Import playlist
    print "Importing playlist..."
    playlistSongs = importPlaylist(playlistFile)

    #Find matches
    print "Finding matches..."
    foundSongs = findMusic(rootdir, playlistSongs)
    files = foundSongs.values()

    #Copy files if matches found
    if files != []:

        #Copy files
        print "Copying files..."
        copyFiles(files, copyDestination)

        #Log found songs
        print "Creating logs..."
        writeFile(foundSongs.keys(), log_foundSongs)

        #Log not found
        notFound = list(set(playlistSongs) - set(foundSongs.keys()))
        if notFound != []:
            writeFile(notFound, log_songsNotFound)

    else:
        print "No matches found."



#Crawl directories to find music files
def findMusic(rootdir, playlistSongs):
    found = {}
    
    for dirPath, subFolders, files in os.walk(rootdir):
        for file in files:
            filePath = os.path.abspath(os.path.join(dirPath, file))
            try:
                if song.isSupportedFileType(filePath):
                    songObj = song.songObjFromFile(filePath)
                    # Add to global list of songs?

                    if testMatch(songObj, playlistSongs):
                        found[songObj] = filePath

            except(mutagen.mp3.error) as exc:
                #Implement error logging with exc
                print "Error! ", exc
                continue

    return found



def testMatch(songObj, playList):
    for song in playList:
        if songObj == song:
            return True
    return False



#Import playlist as song objects
def importPlaylist(file):
    songList = [] 

    # Parse CSV file
    playList = readFile(file)
    for line in playList:
        songObj = song(line)
        songList.append(songObj)

    return songList


def readFile(file):
    songs = []
    keys = []

    with codecs.open(file, 'rb', encoding='utf-8') as f:
        for line in f:
            tagsDict = {}
            tags = [x.rstrip() for x in line.split('\t')]
            
            #Get header row
            if keys == []:
                keys = tags
            #Create ditionary with header row as keys
            else:
                for key, value in zip(keys, tags):
                    tagsDict[key] = value
            if tagsDict != {}:
                songs.append(tagsDict)

    return songs


#Write log files
def writeFile(data, file):
    with codecs.open(file, 'wb', encoding='utf-8') as f:
        output = ("artist", "title", "album", "bitrate", "length")

        f.write(outputFormatter(output))

        for s in data:
            output = (s.artist, s.title, s.album, s.bitrate, s.length)
            f.write(outputFormatter(output))


def outputFormatter(output):
    output = "\t".join(output) + "\n"
    return output



#Copy file to directory
def copyFiles(files, copyDestination):

    #Make directory to receive files
    try:
      os.makedirs(copyDestination)
    except OSError as exception:
      if exception.errno != errno.EEXIST:
          print "Error creating directory!"
          raise

    
    for i, file in enumerate(files):
        try:
            #print os.path.basename(file) 
            shutil.copy2(file, copyDestination) 
            outputStatus(i, len(files))
        except IOError, ex:
            print "IO Error", ex


  
#Status bar
def outputStatus(status, total):
    if status < total:
        sys.stdout.write("%d%%\r" % (int(float(status)/total*100.0)) )
        sys.stdout.flush() 
    else:
        print "100%"


if __name__ == "__main__":
    main()



