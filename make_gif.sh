#!/bin/bash

echo "Making gif..."
ffmpeg -y -r 24 -i ./plots/gasdens%03d.jpg ./plots/animation.gif
