import os
import sys
import glob
from os import listdir
from os.path import isfile, join

if len(sys.argv) != 4:
    print ""
    print "Usage: python picstovideo.py <IMAGES_PATH> <RESOLUTION> <RATE>"
    print "Example: python picstovideo.py /root/User/images/ 1920x1080 4"
    print ""
    sys.exit(0)

folderpath = sys.argv[1]
resolution = sys.argv[2]
rate = sys.argv[3]

if not os.path.isdir(folderpath):
    print "Please enter a folder containing images!"
    sys.exit(0)

if not folderpath.endswith("/"):
    folderpath = folderpath + "/"

onlyfiles = [f for f in listdir(folderpath) if isfile(join(folderpath, f))]
onlyfiles.sort()
mogrifypath = os.popen("which mogrify").read()[:-1]

if len(mogrifypath) == 0:
    print "You need to install mogrify!"
    sys.exit(0)

ffmpegpath = os.popen("which ffmpeg").read()[:-1]

if len(ffmpegpath) == 0:
    print "You need to install ffmpeg!"
    sys.exit(0)

if not os.path.isdir(folderpath + "temp/"):
    os.system("mkdir " + folderpath + "temp/")
else:
    print "Clean up..."
    currentfiles = glob.glob(folderpath + "temp/*")
    for i in currentfiles:
        os.remove(i)

counter = 1

for i in onlyfiles:
    filename = "IMG_" + ("%06d" % (counter,)) + ".jpg"
    counter += 1
    os.system("cp " + folderpath + i + " " + folderpath + "temp/" + filename)
    print "Copied " + i + " as " + filename

print "Resizing pictures to " + resolution
os.system(mogrifypath + " -resize " + resolution + " " + folderpath + "temp/*.jpg")
print "Converting to video..."
os.system(ffmpegpath + " -f image2 -r " + str(rate) + " -i " + folderpath + "temp/" + "IMG_%06d.jpg" + " output_" + resolution + "_" + str(rate) + ".mp4")
print "Generated video successfully!"   
print "Clean up..."

currentfiles = glob.glob(folderpath + "temp/*")

for i in currentfiles:
    os.remove(i)
os.rmdir(folderpath + "temp/")
print "Finished cleaning up"
