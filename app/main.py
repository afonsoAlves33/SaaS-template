from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"It's working"}

@app.get("/a")
def i():
    return "2133"