from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Risk Monitoring System Backend"}
