import support
import sys

source = "."
if len(sys.argv) > 1:
    source = sys.argv[1]

#list = support.fileList(source)
#print list
#list2 = support.findDuplicateFiles(list)
#for file in list2:
#    if len(list2[file]) > 1:
#        print file, ": ", len(list2[file])
#        for subfile in list2[file]:
#            print subfile['path']

filecollection = support.FileCollection()
for name, file in filecollection.files.iteritems():
    for uniquefile in file.uniqueFileList[support.SOURCE]:
        for location in uniquefile.fileLocationList:
            print location.path
filecollection.display()