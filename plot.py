
import logging
import azure.functions as func
from __app__.constants import FORMATS,MIME
from __app__.settings import SETTINGS

from io import BytesIO
from matplotlib import pyplot as plt

def outputPlot(fn):
    plt.style.use(SETTINGS["style"])

    def respondWithPlot(req: func.HttpRequest) -> func.HttpResponse:
        logging.info('Python HTTP trigger function processed a request.')

        fmt = "png" if "fmt" not in req.params.keys() else req.params["fmt"]
        fmt = "png" if fmt not in FORMATS else fmt

        b = BytesIO()

        try:
            fn(**req.params)
        except Exception as e:
            return func.HttpResponse(
                str(e)
            )

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
