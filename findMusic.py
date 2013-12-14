import os
import errno
import sys
import codecs
import shutil

from song import song

import mutagen.mp3




# import difflib
# difflib.get_close_matches(word, possibilities[, n][, cutoff])

def main():
    #program variables
    playlistFile = "/home/nick/tmp/music/playlist.txt"
    rootdir = "/home/nick/tmp/music"
    copyDestination = "/home/nick/tmp/music_found/"
    log_foundSongs = copyDestination + "songs_found.txt"
    log_songsNotFound = copyDestination + "songs_notfound.txt"


    playlistSongs = importPlaylist(playlistFile)
    foundSongs = findMusic(rootdir, playlistSongs)
    files = foundSongs.values()

    copyFiles(files, copyDestination)

    #Found songs
    writeFile(foundSongs.keys(), log_foundSongs)

    #Not found
    notFound = list(set(playlistSongs) - set(foundSongs.keys()))
    if (len(notFound) > 0):
        writeFile(notFound, log_songsNotFound)


    



def findMusic(rootdir, playlistSongs):
    found = {}
    
    for dirPath, subFolders, files in os.walk(rootdir):
        for file in files:
            filePath = os.path.abspath(os.path.join(dirPath, file))
            try:
                if song.isSupportedFileType(filePath):
                    songObj = song.songObjFromFile(filePath)
                    # Add to global list of songs (if advanced search option set?)
                    if testMatch(songObj, playlistSongs):
                        #print songObj.artist + " - " + songObj.title
                        found[songObj] = filePath

            except(mutagen.mp3.error) as exc:
                #Implement error logging with exc
                print "Error! ", exc
                continue


    #print found.values()
    return found




                    

def testMatch(songObj, playList):
    for song in playList:
        if songObj == song:
            return True
    return False




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

            if keys == []:
                keys = tags
            else:
                for key, value in zip(keys, tags):
                    tagsDict[key] = value
            if tagsDict != {}:
                songs.append(tagsDict)

    return songs

def writeFile(data, file):
    with codecs.open(file, 'wb', encoding='utf-8') as f:
        output = ("artist", "title", "album", "bitrate", "length")

        f.write(outputFormatter(output))

        for s in data:
            output = (s.artist, s.title, s.album, s.bitrate, s.length)
            f.write(outputFormatter(output))


def outputFormatter(output):
    line = ""
    for item in output:
        if item != output[-1]:
            line = line + item + "\t"
        else:
            line = line + item + "\n"
    return line




#Copy file to directory
def copyFiles(files, copyDestination):

    #Make directory to receive files
    try:
      os.makedirs(copyDestination)
    except OSError as exception:
      if exception.errno != errno.EEXIST:
          raise

    print "Copying... " 
    
    for file in files:

        print os.path.basename(file) 

        shutil.copy2(file, copyDestination) 

  



if __name__ == "__main__":
    main()



