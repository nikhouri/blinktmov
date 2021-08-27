#!/bin/sh
# makedemo.sh - makes sample BMOVs and demo GIF

# Download Charade https://archive.org/details/Charade19631280x696
# wget https://archive.org/download/Charade19631280x696/Charade-1963.mp4

# Make the full demo movie
# python3 mp42bmov.py Charade-1963.mp4 charade.bmov

# Extract what we want out of the movie
ffmpeg -ss 1:10:56 -t 7 -i Charade-1963.mp4 charadesm.mp4

# Make the small demo movie
python3 mp42bmov.py charadesm.mp4 charadesm.bmov

# Frames folder to hold all the images
mkdir frames

# Convert film extract to GIF
ffmpeg -i charadesm.mp4 -r 10 -vf scale=400:-1 frames/MOVIE-%04d.png

# Colour bars
ffmpeg -i charadesm.mp4 -r 10 -s 8x1 -vf eq=saturation=2 frames/BARS-%04d.png

# Blinkt! video
ffmpeg -ss 0.1 -i blinkt.mp4 -frames 72 -r 10 -vf scale=400:-1 frames/BLINKT-%04d.png

# Scale bars up (pixellated)
mogrify -scale 400x20\! frames/BARS-*.png

# Combine movie/bars/blinkt frames: https://legacy.imagemagick.org/Usage/anim_mods/#append
for i in `seq -f '%04g' 1 72`; do \
	convert frames/MOVIE-$i.png frames/BARS-$i.png frames/BLINKT-$i.png -append frames/charadedemo-$i.png
done

# Animate the combined frames
gifski --fps 10 -o charadedemo.gif frames/charadedemo-*.png --quality 80

# Clean up
rm -r frames