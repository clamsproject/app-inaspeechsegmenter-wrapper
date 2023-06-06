"""
The purpose of this file is to define the metadata of the app with minimal imports. 

DO NOT CHANGE the name of the file
"""
import re
from mmif import DocumentTypes, AnnotationTypes

from clams.appmetadata import AppMetadata

timeunit = 'milliseconds'

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
        identifier='inaaudiosegmenter-wrapper'
    )
    metadata.add_input_oneof(DocumentTypes.AudioDocument, DocumentTypes.VideoDocument)
    metadata.add_output(AnnotationTypes.TimeFrame, timeunit=timeunit)
    return metadata


# DO NOT CHANGE the main block
if __name__ == '__main__':
    import sys
    sys.stdout.write(appmetadata().jsonify(pretty=True))
