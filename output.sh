#!/bin/bash
set -eu
mkdir -p sample_video_output
mkdir -p ina_runtime

# pip install clams-python

for file in /Users/Brenda/Documents/GitHub/app-inaspeechsegmenter-wrapper/sample_video_input/*.mmif; do
    # get filename without path, "${filename%.*}" is used for output id to takeout .mp4 extension
    filename=$(basename $file)
    echo "processing file: $filename"

    # clams source audio:/sample_videos/$filename > sample_video_input/"${filename%.*}"_input.mmif
    curl -H "Accept: application/json" -X POST -d@sample_video_input/"${filename%.*}".mmif -s http://localhost:5005?pretty > sample_video_output/"${filename%.*}"_ina.mmif

    # # keep track running time: currently using standard error, might be changed later
    # # redirect time output to subdir ./time
    { time curl -H "Accept: application/json" -X POST -d@sample_video_input/"${filename%.*}".mmif -s http://localhost:5005?pretty > sample_video_output/"${filename%.*}"_ina.mmif 2> ina_runtime/"${filename%.*}".stderr ; } 2> ina_runtime/"${filename%.*}".txt
done
