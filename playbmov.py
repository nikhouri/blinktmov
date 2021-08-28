#!/usr/bin/python3
# playbmov.py - play a Blinkt! "movie" file .bmov

import sys
import time
import json
import gzip
import blinkt

FRAMERATE = 0 # Already plays too slow!
FRAMESKIP = 7 # Skip every Nth frame
MAXBRIGHT = 0.950 # Very bright!
MINBRIGHT = 0.033 # Lowest it seems to go is 0.033

if __name__ == '__main__':

	if (len(sys.argv) >= 2): # Check if a file name is given 
		bmovfile = sys.argv[1]
	else:
		print("Usage: playmbov.py [bmov_filename]")
		quit()

	# Import from compressed file - see: https://stackoverflow.com/a/39451012
	print('### Reading BMOV')
	with gzip.open(bmovfile, 'r') as fin:
		bmov = json.loads(fin.read().decode('utf-8'))
	print('### Movie length is ' + str(len(bmov)) + ' frames, '
		  + str(round(len(bmov) / 24 / 60,1)) + " minutes")

	# Loop thorugh and play bmov
	print('### Playing BMOV')
	print('### 0%      25%       50%       75%     100%')
	print('### ++------++--------++--------++--------++')
	sys.stdout.write('### ..')
	sys.stdout.flush()
	lastpct=0
	for i in range(len(bmov)):
		if round(i/len(bmov)*100,0)//5 > lastpct:
		 	sys.stdout.write('..')
		 	sys.stdout.flush()
		 	lastpct += 1
		if (i % FRAMESKIP != 0): # Skip every 5th update
			for j in range(blinkt.NUM_PIXELS):
				r, g, b = bmov[i][j]
				blinkt.set_pixel(j, r, g, b, max(min((r+g+b)/765*MAXBRIGHT,1), MINBRIGHT))
			blinkt.show()
		time.sleep(FRAMERATE)
	print('\n### Done! Thank you for your custom')