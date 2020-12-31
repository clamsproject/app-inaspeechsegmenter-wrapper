# app-ina-segmenter v0.1.0
This is a CLAMS app that wraps the [inaSpeechSegmenter tool](https://github.com/ina-foss/inaSpeechSegmenter).

To run the app in this repository, either use the Dockerfile to install its dependencies 
or make sure the run environment corresponds to the instructions in the Dockerfile.

To run the demo on the provided mp3 file, first build the Docker image, then run the outer demo script:

```
$ docker build -t app-ina-segmenter:latest -t app-ina-segmenter:0.1.0 .
$ chmod +x outerdemo.sh
$ ./outerdemo.sh
```

Open the newly created `demo/results` to see the generated tsv file (for comparison) and MMIF files.

To run the app as a Flask app, build the image and run the container in the usual CLAMS-y way.

Command line API for `app.py`:

```
usage: app.py [-h] [--once PATH] [--pretty] [--save-tsv]

optional arguments:
  -h, --help   show this help message and exit
  --once PATH  Use this flag if you want to run the segmenter on a path you
               specify, instead of running the Flask app.
  --pretty     Use this flag to return "pretty" (indented) MMIF data.
  --save-tsv   Use this flag to preserve the intermediary TSV file generated
               by the segmenter.
```
