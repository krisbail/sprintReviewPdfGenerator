# coding: utf8


from chardet.universaldetector import UniversalDetector

from ReportConfigParser import *
from os import walk, system
from os.path import join, basename, exists, isdir, splitext
from shutil import copy2

config = ReportConfiguration(26)

work_path = config.work_path()
detector = UniversalDetector()
for (import_path, dirnames, filenames) in walk(config.import_path()):
    for filename in filenames:
        detector.reset()
        for line in file(join(import_path, filename), 'rb'):
            detector.feed(line)
            if detector.done: break
        detector.close()
        print filename
        encoding = detector.result["encoding"]
        print detector.result["encoding"]
        if encoding != "utf-8":
            system("iconv -f %s -t UTF-8 '%s' > '%s'" % (encoding, join(import_path, filename), join(work_path, filename)))
        else:
            copy2(join(import_path, filename), join(work_path, filename))


        #print "%s -> %s" % (filename, chardet.detect())
        #if file_extension == ".csv":
            # system("iconv -f ISO-8859-1 -t UTF-8 '%s' > '%s'" % (join(import_path, filename), join(work_path, filename)))
            #copy2(join(import_path, filename), join(work_path, filename))