import argparse
from typing import Union

from clams import Restifier
from clams.app import ClamsApp
from clams.appmetadata import AppMetadata
from inaSpeechSegmenter import Segmenter
from mmif import DocumentTypes, AnnotationTypes, Mmif

__version__ = '0.2.2'


class InaSegmenter(ClamsApp):

    def _appmetadata(self):
        metadata = AppMetadata(
            name="inaSpeechSegmenter Wrapper",
            description="inaSpeechSegmenter is a CNN-based audio segmentation toolkit. The original software can be "
                        "found at https://github.com/ina-foss/inaSpeechSegmenter .",
            app_version=__version__,
            wrappee_version='0.6.7',
            license='MIT',
            wrappee_license='MIT',
            identifier=f"http://apps.clams.ai/inaaudiosegmenter-wrapper/{__version__}",
        )
        metadata.add_input(DocumentTypes.AudioDocument)
        metadata.add_output(AnnotationTypes.TimeFrame)
        return metadata

    def _annotate(self, mmif: Union[str, dict, Mmif], **runtime_params) -> Mmif:
        if not isinstance(mmif, Mmif):
            mmif = Mmif(mmif)
        conf = self.get_configuration(**runtime_params)

        # prep ina 
        ina = Segmenter()

        # get AudioDocuments with locations
        for audiodoc in [document for document in mmif.documents
                         if document.at_type == DocumentTypes.AudioDocument
                            and len(document.location) > 0]:
            filename = audiodoc.location_path()
            segments = ina(filename)

            v = mmif.new_view()
            self.sign_view(v, conf)
            v.new_contain(AnnotationTypes.TimeFrame, {'timeUnit': 'milliseconds',
                                                      'document': audiodoc.id})
            for label, start_sec, end_sec in segments:
                a = v.new_annotation(AnnotationTypes.TimeFrame)

                a.add_property('start', int(start_sec * 1000))
                a.add_property('end', int(end_sec * 1000))
                if label == 'male' or label == 'female':
                    a.add_property('gender', label)
                    a.add_property('frameType', 'speech')
                else:
                    a.add_property('frameType', label)
        return mmif


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--production',
                        action='store_true')
    parsed_args = parser.parse_args()

    segmenter_app = InaSegmenter()
    segmenter_service = Restifier(segmenter_app)
    if parsed_args.production:
        segmenter_service.serve_production()
    else:
        segmenter_service.run()
