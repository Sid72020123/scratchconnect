from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Error": False, "Message": "ScratchConnect Additional APIs", "Credits": "Made by @Sid72020123 on Scratch"}

