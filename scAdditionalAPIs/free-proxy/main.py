from random import randint
from requests import get
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/")
def root():
    return {"Error": False, "Message": "Free Proxy is Running!", "Credits": "Made by @Sid72020123 on Scratch"}


@app.get("/get")
def proxy(url: str, request: Request, response: Response):
    headers = {
        "User-Agent": f"Proxy - {randint(1, 100)}!"
    }
    request_headers = dict(request.headers)
    args = dict(request.query_params.multi_items())
    args.pop("url")
    try:
        r = get(url, params=args, headers=headers)
        raw_headers = r.raw.headers.items()
        excluded_headers = ["content-encoding", "content-length"]
        headers = {}
        for (name, value) in raw_headers:
            if name.lower() not in excluded_headers:
                headers[name] = value
        return Response(content=r.content, status_code=r.status_code, headers=headers)
    except Exception as E:
        return Response(content="Internal Server Error - " + str(E), status_code=500)
