# Blinkt! Movie Player

Squishes down and plays a video on Pimoroni's excellent [Blinkt!](https://shop.pimoroni.com/products/blinkt) LED strip for the Raspberry Pi. Demo below shows the original video, representitive pixels, and output on the Blinkt!

![Blinkt! Movie Player Demo](charadedemo.gif)

Colour mapping from movies to the Blinkt! LEDs needs some work.

## Scripts

* `mp42bmov.py` - Converts an MP4 into a BMOV movie
* `playbmov.py` - Plays a BMOV movie on Blinkt!
* `makedemo.sh` - creates the demo image (uncomment d/l first)

## Uses

* Ambient film lighting
* Fake TV lighting while you're out

## Requirements

* Working installs of `ffmpeg`, `ImageMagick`
* Blinkt! and Pillow libraries for Python 3