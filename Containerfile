# Use the same base image version as the clams-python python library version
FROM ghcr.io/clamsproject/clams-python-ffmpeg-tf2:1.0.2
# See https://github.com/orgs/clamsproject/packages?tab=packages&q=clams-python for more base images
# IF you want to automatically publish this image to the clamsproject organization, 
# 1. you should have generated this template without --no-github-actions flag
# 1. to add arm64 support, change relevant line in .github/workflows/container.yml 
#     * NOTE that a lots of software doesn't install/compile or run on arm64 architecture out of the box 
#     * make sure you locally test the compatibility of all software dependencies before using arm64 support 
# 1. use a git tag to trigger the github action. You need to use git tag to properly set app version anyway

################################################################################
# DO NOT EDIT THIS SECTION
ARG CLAMS_APP_VERSION
ENV CLAMS_APP_VERSION ${CLAMS_APP_VERSION}
################################################################################

################################################################################
# clams-python base images are based on debian distro
# install more system packages as needed using the apt manager
RUN apt update && apt install -y ffmpeg libsndfile1
# download keras models to be used by the INA speech segmenter
ARG u='https://github.com/ina-foss/inaSpeechSegmenter/releases/download/models/'
ADD ${u}keras_male_female_cnn.hdf5 \
    ${u}keras_speech_music_cnn.hdf5 \
    ${u}keras_speech_music_noise_cnn.hdf5 \
    /root/.keras/inaSpeechSegmenter/

################################################################################

################################################################################
# main app installation
COPY ./ /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
# issue with old keras that comes with ina-segmenter (https://github.com/keras-team/keras/issues/14632)
RUN python3 -m pip uninstall -y keras keras-nightly
RUN python3 -m pip install --upgrade --force-reinstall $(grep tensorflow requirements.txt)

# default command to run the CLAMS app in a production server 
CMD ["python3", "app.py", "--production"]
################################################################################
