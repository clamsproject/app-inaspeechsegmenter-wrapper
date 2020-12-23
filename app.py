# app-ina-segmenter version 0.1.0
# author: Angus L'Herrou
# org: CLAMS team
import json
import os
import tempfile
import csv
from io import StringIO

from clams import Restifier
from mmif import DocumentTypes, AnnotationTypes

from inaSpeechSegmenter import Segmenter

import app_audio_segmenter.app
from app_audio_segmenter.app import Segmenter as ClamsSegmenter


APP_VERSION = '0.1.0'
WRAPPED_IMAGE = 'clamsproject/clams-python:0.1.8'
MEDIA_DIRECTORY = '/segmenter/data'
CSV_DIRECTORY = '/segmenter/csv'
SEGMENTER_DIR = '/segmenter/acoustic-classification-segmentation'
TIME_FRAME_PREFIX = 'tf'
with open('demuxers.json', encoding='utf8') as demuxers:
    SEGMENTER_ACCEPTED_EXTENSIONS = set(json.load(demuxers))
    app_audio_segmenter.app.SEGMENTER_ACCEPTED_EXTENSIONS = SEGMENTER_ACCEPTED_EXTENSIONS


class InaSegmenter(ClamsSegmenter):
    def setupmetadata(self) -> dict:
        return {
            "name": "inaSpeechSegmenter Audio Segmenter",
            "description": "tbd",
            "vendor": "Team CLAMS",
            "iri": f"http://mmif.clams.ai/apps/ina-segmenter/{APP_VERSION}",
            "wrappee": WRAPPED_IMAGE,
            "requires": [DocumentTypes.AudioDocument.value],
            "produces": [
                AnnotationTypes.TimeFrame.value
            ]
        }


def segment(save_tsv=False) -> str:
    seg = Segmenter(detect_gender=False)
    files = os.listdir(MEDIA_DIRECTORY)
    dir = CSV_DIRECTORY if save_tsv else tempfile.mkdtemp()
    if save_tsv:
        for file in os.listdir(CSV_DIRECTORY):
            os.unlink(file)
    t_batch_dur, nb_processed, avg, lmsg = seg.batch_process(files, [os.path.join(dir, file) for file in files])
    result = StringIO()
    writer = csv.writer(result, delimiter='\t')
    segmentation_paths = os.listdir(dir)
    assert len(segmentation_paths) == len(files), ("didn't get the right number of segmentations "
                                                   f"(files {len(files)}, segmentations {len(segmentation_paths)}")
    for file_name, csv_name in zip(files, segmentation_paths):
        abs_file_name = os.path.join(MEDIA_DIRECTORY, file_name)
        out_row = [abs_file_name]
        with open(csv_name, encoding='utf8') as csv_file:
            segmentation = csv.DictReader(csv_file, delimiter='\t')
            for row in segmentation:
                if row['labels'] == 'speech':
                    out_row.extend([row['start'], row['stop']])
        out_row.append('speech_ratio: 0% (0 / 0)')  # we don't care about speech ratio
        writer.writerow(out_row)
    return result.read()


if __name__ == '__main__':
    ina_app = InaSegmenter()
    ina_service = Restifier(ina_app)
    ina_service.run()
