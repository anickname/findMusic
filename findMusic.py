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
    playlistFile = "/home/nick/tmp/music/playlist.csv"
    rootdir = "/home/nick/tmp/music"
    copyDestination = "/home/nick/tmp/music_found/"


    playlistSongs = importPlaylist(playlistFile)
    foundSongs = findMusic(rootdir, playlistSongs)
    files = foundSongs.values()

    copyFiles(files, copyDestination)





def findMusic(rootdir, playlistSongs):
    found = {}
    
    for dirPath, subFolders, files in os.walk(rootdir):
        for file in files:
            s = song()
            filePath = os.path.abspath(os.path.join(dirPath, file))
            try:
                if s.isSupportedFileType(filePath):
                    s.songObjFromTags(filePath)
                    songObj = s
                    # Add to global list of songs (if advanced search option set?)
                    if testMatch(songObj, playlistSongs):
                        # print songObj.artist + " - " + songObj.title
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




def importPlaylist(file):
    songList = [] 

    # Parse CSV file
    playList = readFile(file)
    for line in playList:
        s = song()
        s.songObjFromPlaylist(line)
        songList.append(s)

    return songList


def readFile(file):
    songs = []
    keys = []

    with codecs.open(file, 'rb', encoding='utf-8') as f:
        for line in f:
            tagsDict = {}
            tags = [x.rstrip() for x in line.split(',')]

            if keys == []:
                keys = tags
            else:
                for key, value in zip(keys, tags):
                    tagsDict[key] = value
            if tagsDict != {}:
                songs.append(tagsDict)

    return songs


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



