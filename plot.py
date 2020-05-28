
import logging
import azure.functions as func
from __app__.constants import FORMATS,MIME
from io import BytesIO
from matplotlib import pyplot as plt

def outputPlot(fn):
    def respondWithPlot(req: func.HttpRequest) -> func.HttpResponse:
        logging.info('Python HTTP trigger function processed a request.')

        fmt = "png" if "fmt" not in req.params.keys() else req.params["fmt"]
        fmt = "png" if fmt not in FORMATS else fmt

        b = BytesIO()

        fn()

        plt.savefig(b,format=fmt)
        b.seek(0)

        return func.HttpResponse(
            b.read(),
            headers={
                "Content-Type": MIME[fmt]
            },
            status_code=200
        )
    return respondWithPlot
