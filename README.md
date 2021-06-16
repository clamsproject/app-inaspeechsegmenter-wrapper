# INA-Segmenter for CLAMS

This is a CLAMS app that wraps the [inaSpeechSegmenter tool](https://github.com/ina-foss/inaSpeechSegmenter).


### Requirement

#### system packages
* libsndfile
* ffmpeg

On Ubuntu, you can installed these by 

``` bash
apt install ffmpeg libsndfile1
```

For other OSs, please refer to the supported package managers to install system libraries.

#### python packages 

Install dependencies using [`requirements.txt`](requirements.txt).

``` bash
pip install -r requirements.txt
```

### Usage

Run [`app.py`](app.py) to start a server. INA segmenter will be running as a HTTP server on Werkzeug. If you need to run it for production, you can use `--production` flag to use `gunicorn` instead of Werkzeug. 
Once a server is running, you can send `POST` request with a [MMIF](https://mmif.clams.ai) file to `http://localhost:5000` to get audio files annotated with segmentation. For example, using `curl` command, 

``` bash 
curl -d@localaudios.mmif localhost:5000
```

If you are not sure how to create a MMIF file from your source audio files, try `clams` command (installed via `requirements.txt`). 

### Docker
If you use docker, you can build a a docker image using enclosed [`Dockerfile`](Dockerfile). Then you can start a container. When you do so, you would want to expose the port (for example `-p 5000:5000`) and to mount the data directory at the correct location encoded in input MMIF files (for example `-v /home/my/local/audio/directory:/data` when in the MMIF you have `"location": "file:///data/my-audio-to-segment.mp3"`).
