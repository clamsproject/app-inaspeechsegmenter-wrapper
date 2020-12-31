FROM nvidia/cuda:11.1-cudnn8-runtime-ubuntu18.04

LABEL maintainer="CLAMS Team <admin@clams.ai>"

# Install package app dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        python3-dev \
        python3-pip \
        ffmpeg \
        perl

# Upgrade pip to latest version (pip version must be >19.0 for tensorflow 2)
RUN python3 -m pip install --upgrade pip

RUN mkdir /segmenter
COPY . /segmenter
WORKDIR /segmenter

# Regenerate supported file types for currently installed ffmpeg version
RUN echo "["$(ffmpeg -loglevel quiet -demuxers | awk '$1 == "D" {print "\"""."$2"\""}' | perl -pe 'chomp if eof' | tr '\n' ',')"]" > demuxers.json

RUN mkdir ./data

# Install python app dependencies
RUN python3 -m pip install -r requirements.txt

# Clone base segmenter into ./app_audio_segmenter/
RUN git clone --depth 1 --branch 1.1 https://github.com/clamsproject/app-audio-segmenter.git app_audio_segmenter

# Catch any stray app dependencies from the base segmenter
RUN python3 -m pip install -r ./app_audio_segmenter/requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]
