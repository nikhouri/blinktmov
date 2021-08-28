#!/usr/bin/python3
# mp4tobmov.py - convert an mp4 to a Blinkt! "movie" file .bmov

import sys
import os
import subprocess
import shutil
import time
import uuid
import json
import gzip
from PIL import Image

if __name__ == "__main__":

   # Check to make sure we've been given the right # of parameters
   if (len(sys.argv) >= 3):
      mp4file = sys.argv[1]
      bmovfile = sys.argv[2]
   else:
      print("Usage: mp4tobmov.py [mp4_filename] [bmov_filename]")
      quit()

   # Create new folder for BMP files
   print('### Creating folder for BMP files')
   bmpdir = str(uuid.uuid4())
   os.mkdir(bmpdir)
   
   # Run ffmpeg to export 8-pixel wide BMP files of each movie frame into
   # a new randomly named directory
   print('### Calling ffmpeg to export BMP files to ' + bmpdir)
   subprocess.run(["ffmpeg", "-i", mp4file, "-r", "24", "-s", "8x1", "-vf", 
                   "eq=saturation=2", "-f", "image2", bmpdir + "/image-%09d.bmp"])

   # Get a list of all bmp files
   bmplist = os.listdir(bmpdir)
   bmplist.sort()

   # Hang on a few secs so OS can catch up
   time.sleep(5)

   # Loop over all files in target directory and extract pixels
   print('### Extracting pixel data')
   allpixarr = []
   for filename in bmplist:
      # Load up the pixel map if we have a bmp
      if ".bmp" in filename:
         bmpimg = Image.open(bmpdir + "/" + filename)
         pixmap = bmpimg.load()
      # Add each pixel to a pixel array
      pixarr = []
      for i in range(8):
         pixarr.append(pixmap[i,0])
      # Append each pixel array to our big list
      allpixarr.append(pixarr)

   # Export to compressed file - see: https://stackoverflow.com/a/39451012
   print('### Writing BMOV')
   with gzip.open(bmovfile, 'w') as fout:
       fout.write(json.dumps(allpixarr).encode('utf-8'))

   # Clean up: delete BMP folder
   print('### Deleting temp BMP files')
   shutil.rmtree(bmpdir)

   # Done
   print('### Done! Thank you for your custom')