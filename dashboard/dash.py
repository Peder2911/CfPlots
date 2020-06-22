import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        """
        <h1>Look at this graph!</h1>
        <img src="/api/pie" alt="">
        """,
        headers={
            "Content-Type":"text/html"
        },
        status_code=200
    )
