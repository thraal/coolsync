import os
import hashlib
import uuid
from collections import defaultdict

SOURCE = 'Source'
DEST = 'Destination'

locationtype = frozenset([SOURCE, DEST])

class FileLocation:
    'unique location for a file'
    uniqueFileId = 0
    path = ''
    size = 0
    creationDate = 0
    hash = 0
    parentUniqueFile = None

    def __init__(self, parentUniqueFile, uniqueFileId, path, size, creationDate):
        self.uniqueFileId = uniqueFileId
        self.path = path
        self.size = size
        self.creationDate = creationDate
        self.parentUniqueFile = parentUniqueFile

    def __repr__(self):
        return "placeholder"

    def display(self):
        print "        Location uniqueFileID: ", self.uniqueFileId
        print "                 path:         ", self.path
        print "                 size:         ", self.size
        print "                 creationDate: ", self.creationDate
        print "                 hash:         ", self.hash

    def calculateHash(self):
        hasher = hashlib.md5()
        filepath = os.path.join(self.path, self.parentUniqueFile.name)
        try:
            with open(filepath) as openfile:
                buf = openfile.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except:
            print "Error generating MD5 hash: ", filepath

class UniqueFile:
    'Unique File object, collection FileLocation objects'
    id = 0
    name = ''
    mappedId = 0
    skip = False

    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.fileLocationList = []

    def add(self, path, size, creationdate):
        self.fileLocationList.append(FileLocation(self.id, self, path, size, creationdate))

    def display(self):
        print "    UniqueFile ID:              ", self.id
        print "               name:            ", self.name
        print "               mappedId:        ", self.mappedId
        print "               skip:            ", self.skip
        print "               number of paths: ", len(self.fileLocationList)
        for location in self.fileLocationList:
            location.display()

    def map(self, otherUniqueFile):
        self.mappedId = otherUniqueFile.mappedId

class File:
    'super File object, containing source and target UniqueFile object lists'
    name = ''

    def __init__(self, name):
        self.name = name
        self.uniqueFileList = {SOURCE: [], DEST: []}

    def add(self, locationtype, name, path, size, creationdate):
        newuniquefile = UniqueFile(name)
        newuniquefile.add(path, size, creationdate)
        self.uniqueFileList[locationtype].append(newuniquefile)


    def display(self):
        print "File name: ", self.name
        for locationtype, filelist in self.uniqueFileList.iteritems():
            print "     number of unique files in ", locationtype, ": ", len(filelist)
            for uniquefile in filelist:
                uniquefile.display()

class FileCollection:
    files = {}

    def display(self):
        print "File Collection:"
        print ""
        for name, file in self.files.iteritems():
            file.display()

    def add(self, locationtype, name, path, size, creationdate):
        file = None
        if name in self.files:
            file = self.files[name]
        else:
            file = File(name)
            self.files[name] = file
        file.add(locationtype, name, path, size, creationdate)

    def fill(self, locationtype, source = "."):
        for path, dirnames, filenames in os.walk(source):
            for filename in filenames:
                try:
                    filepath = os.path.join(path, filename)
                    print filename
                    self.add(locationtype, filename, path, os.path.getsize(filepath), os.path.getctime(filepath))
                except:
                    print "File access error: " + filename
        return self.files

def findDuplicateFiles(files):
    mydict = defaultdict(list)
    for file in files:
        filename = file['name']
        filepath = file['path']
        filesize = file['size']
        mydict[filename].append({ 'path': filepath, 'size': filesize })
        # mydict[key['name']].append[[key['path'], key['size']]]
        print file
        print file['name'], ", ", file['path'], ", ", file['size']
    return mydict
