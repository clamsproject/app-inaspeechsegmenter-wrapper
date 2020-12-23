FROM clamsproject/clams-python:0.1.8

LABEL maintainer="Angus L'Herrou <piraka@brandeis.edu>"

RUN apt-get update && apt-get install -y ffmpeg && apt-get install perl

RUN mkdir /segmenter
COPY . /segmenter
WORKDIR /segmenter

RUN echo "["$(ffmpeg -loglevel quiet -demuxers | awk '$1 == "D" {print "\""$2"\""}' | perl -pe 'chomp if eof' | tr '\n' ',')"]" > demuxers.json

RUN mkdir ./data

RUN pip install -r requirements.txt

RUN git clone --depth 1 --branch v0.1.0 https://github.com/clamsproject/app-audio-segmenter.git app_audio_segmenter

RUN pip install -r ./app_audio_segmenter/requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
