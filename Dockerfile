FROM clamsproject/clams-python-ffmpeg:0.4.4

LABEL maintainer="CLAMS Team <admin@clams.ai>"
LABEL issues="https://github.com/clamsproject/app-inaspeechsegmenter-wrapper/issues"

RUN apt update && apt install -y ffmpeg libsndfile1
COPY . /app
WORKDIR /app

# Install python app dependencies
RUN python3 -m pip install -r requirements.txt
# issue with old keras that comes with ina-segmenter (https://github.com/keras-team/keras/issues/14632)
RUN python3 -m pip uninstall -y keras keras-nightly
RUN python3 -m pip install --upgrade --force-reinstall $(grep tensorflow requirements.txt)

CMD ["python3", "app.py", "--production"]
