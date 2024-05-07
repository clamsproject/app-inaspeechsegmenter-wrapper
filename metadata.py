"""
The purpose of this file is to define the metadata of the app with minimal imports. 

DO NOT CHANGE the name of the file
"""
import re
from mmif import DocumentTypes, AnnotationTypes

from clams.app import ClamsApp
from clams.appmetadata import AppMetadata

timeunit = 'milliseconds'
ina_original_labels = 'noEnergy female male noise music'.split()
wrapper_labels = 'silence speech noise music'.split()


# DO NOT CHANGE the function name 
def appmetadata() -> AppMetadata:
    
    metadata = AppMetadata(
        name="inaSpeechSegmenter Wrapper",
        description="inaSpeechSegmenter is a CNN-based audio segmentation toolkit. The original software can be "
                    "found at https://github.com/ina-foss/inaSpeechSegmenter .",
        app_license='MIT',
        analyzer_license='MIT',
        analyzer_version=[l.strip().rsplit('==')[-1] for l in open('requirements.txt').readlines() if re.match(r'^inaSpeechSegmenter==', l)][0],
        url='https://github.com/clamsproject/app-inaspeechsegmenter-wrapper',
        identifier='inaspeechsegmenter-wrapper'
    )
    metadata.add_input_oneof(DocumentTypes.AudioDocument, DocumentTypes.VideoDocument)
    metadata.add_output(AnnotationTypes.TimeFrame, timeunit=timeunit, labelset=wrapper_labels)\
        .add_description(f'The INA semgmenter uses 5-way classification ({ina_original_labels}) and this wrapper '
                         f'remaps the labels to {wrapper_labels}, by 1) renaming `noEnergy` to `silence` 2) collapsing '
                         f'`female` and `male` into `speech` (leaving additional `gender` property). Note that the '
                         f'time frame annotations do not exhaustively cover the input audio, but only the segments.')
    metadata.add_parameter(name='minTFDuration', type='integer', default=0,
                           description='minimum duration of a TimeFrame in milliseconds')
    metadata.add_parameter(name='silenceRatio', type='integer', default=3,
                           description='percentage ratio (0-100) of audio energy to to determine silence, ratio to '
                                       'mean every of the input audio.')
    return metadata


# DO NOT CHANGE the main block
if __name__ == '__main__':
    import sys
    metadata = appmetadata()
    for param in ClamsApp.universal_parameters:
        metadata.add_parameter(**param)
    sys.stdout.write(metadata.jsonify(pretty=True))
