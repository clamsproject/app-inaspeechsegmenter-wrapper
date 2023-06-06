import argparse
from typing import Union

from clams import Restifier
from clams.app import ClamsApp
from clams.appmetadata import AppMetadata
from inaSpeechSegmenter import Segmenter
from mmif import DocumentTypes, AnnotationTypes, Mmif

import metadata


class INASSWrapper(ClamsApp):

    def _appmetadata(self):
        pass

    def _annotate(self, mmif: Union[str, dict, Mmif], **runtime_params) -> Mmif:
        if not isinstance(mmif, Mmif):
            mmif = Mmif(mmif)
        conf = self.get_configuration(**runtime_params)

        # prep ina 
        ina = Segmenter()

        # get AudioDocuments with locations
        for media in mmif.get_documents_by_type(DocumentTypes.AudioDocument) + mmif.get_documents_by_type(DocumentTypes.VideoDocument):
            filename = media.location_path()
            segments = ina(filename)

            v = mmif.new_view()
            self.sign_view(v, conf)
            v.new_contain(AnnotationTypes.TimeFrame, timeUnit=metadata.timeunit, document=media.id)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", action="store", default="5000", help="set port to listen"
    )
    parser.add_argument("--production", action="store_true", help="run gunicorn server")

    parsed_args = parser.parse_args()

    segmenter = INASSWrapper()
    segmenter_app = Restifier(segmenter, port=parsed_args.port)
    if parsed_args.production:
        segmenter_app.serve_production()
    else:
        segmenter_app.run()
