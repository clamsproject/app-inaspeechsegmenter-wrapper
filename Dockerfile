FROM clamsproject/clams-python-tf2:0.4.1

LABEL maintainer="CLAMS Team <admin@clams.ai>"
LABEL issues="https://github.com/clamsproject/app-ina-segmenter/issues"

RUN apt update && apt install -y ffmpeg libsndfile1
COPY . /app
WORKDIR /app

# Install python app dependencies
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "app.py", "--production"]
