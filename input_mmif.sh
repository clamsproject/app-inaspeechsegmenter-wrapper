#!/bin/bash
set -eu
# mkdir -p sample_video_input

# pip install clams-python

for file in /Users/Brenda/Documents/GitHub/app-inaspeechsegmenter-wrapper/sample_videos/*.mp4; do
    # get filename without path, "${filename%.*}" is used for output id to takeout .mp4 extension
    filename=$(basename $file)
    echo "processing file: $filename"

    clams source audio:/Users/Brenda/Documents/GitHub/app-inaspeechsegmenter-wrapper/sample_videos/$filename > sample_video_input/"${filename%.*}"_input.mmif

done
