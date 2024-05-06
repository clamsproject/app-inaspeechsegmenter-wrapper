import argparse
import logging

from clams import Restifier
from clams.app import ClamsApp
from inaSpeechSegmenter import Segmenter
from mmif import DocumentTypes, AnnotationTypes, Mmif

import metadata


class INASSWrapper(ClamsApp):

    def _appmetadata(self):
        pass

    def _annotate(self, mmif: Mmif, **parameters) -> Mmif:
        if not isinstance(mmif, Mmif):
            mmif = Mmif(mmif)

        # prep ina 
        ina = Segmenter()

        # get AudioDocuments with locations
        for document in mmif.get_documents_by_type(DocumentTypes.AudioDocument) + mmif.get_documents_by_type(DocumentTypes.VideoDocument):
            filename = document.location_path()
            segments = ina(filename)

            v = mmif.new_view()
            self.sign_view(v, parameters)
            v.new_contain(AnnotationTypes.TimeFrame, timeUnit=metadata.timeunit, document=document.id)
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


def get_app():
    """
    This function effectively creates an instance of the app class, without any arguments passed in, meaning, any 
    external information such as initial app configuration should be set without using function arguments. The easiest
    way to do this is to set global variables before calling this. 
    """
    return INASSWrapper()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", action="store", default="5000", help="set port to listen")
    parser.add_argument("--production", action="store_true", help="run gunicorn server")

    parsed_args = parser.parse_args()

    # create the app instance
    # if get_app() call requires any "configurations", they should be set now as global variables
    # and referenced in the get_app() function. NOTE THAT you should not change the signature of get_app()
    app = get_app()

    http_app = Restifier(app, port=int(parsed_args.port))
    # for running the application in production mode
    if parsed_args.production:
        http_app.serve_production()
    # development mode
    else:
        app.logger.setLevel(logging.DEBUG)
        http_app.run()
