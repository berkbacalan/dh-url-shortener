from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Default backend with status 200"