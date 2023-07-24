# INA-Segmenter for CLAMS

## Description

This is a CLAMS app that wraps the [inaSpeechSegmenter tool](https://github.com/ina-foss/inaSpeechSegmenter).

## User instruction

General user instructions for CLAMS apps is available at [CLAMS Apps documentation](https://apps.clams.ai/clamsapp).

### System requirements

* libsndfile
* ffmpeg

On Ubuntu, you can install these by 

``` bash
apt install ffmpeg libsndfile1
```

For other OSs, please refer to the supported package managers to install system libraries.

### Python packages

Install dependencies using [`requirements.txt`](requirements.txt).

``` bash
pip install -r requirements.txt
```

If you encounter an `AttributeError` from `module 'keras.utils.generic_utils'`, you might need to re-install `tensorflow` after deleting `keras`. 

```
pip uninstall -y keras keras-nightly
pip install --upgrade --force-reinstall $(grep tensorflow requirements.txt)
```
