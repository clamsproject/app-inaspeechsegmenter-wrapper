

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

Run [`app.py`](app.py) to start a server. The INA segmenter will be running as a HTTP server on Werkzeug. If you need to run it for production, you can use the `--production` flag to use `gunicorn` instead of Werkzeug. Once a server is running, you can send a `POST` request with a [MMIF](https://mmif.clams.ai) file to `http://localhost:5000` to get audio files annotated with segmentation. For example, using the `curl` command in a terminal,

``` bash 
curl -d@localaudios.mmif localhost:5000
```

If you are not sure how to create a MMIF file from your source audio files, try the `clams` command (installed via `requirements.txt`).

### Docker
If you use docker, you can build a docker image using enclosed [`Dockerfile`](Dockerfile).

```
docker build -t ina-segmenter .
```

When building the container make sure to increase the Docker memory resources by going into the Docker Dashboard, select "Resources" and set the memory allotment to 4.00 GB. Without that the build process may run into a memory error and exit with code 137.

Then you can start a container. When you do so, you would want to expose the port (for example `-p 5000:5000`) and to mount the data directory at the correct location encoded in input MMIF files (for example `-v /my/local/audio/directory:/data` when in the MMIF you have `"location": "file:///data/my-audio-to-segment.mp3"`). Use `--name` if you want to control the name of the container.

```
docker run -d -p 5000:5000 -v /my/local/audio/directory:/data --name ina-segmenter ina-segmenter
```

