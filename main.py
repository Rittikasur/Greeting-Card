from fastapi import FastAPI
from fastapi.responses import Response
from app.model.model import generate_birthday_card, generate_card
from app.model.model import __version__ as model_version


app = FastAPI()

@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}


@app.post("/prompt")
def predict(paload:dict):
    language = generate_birthday_card(int(paload["ngs"]))
    return {"language": language}


@app.post("/generate")
def generate(paload:dict):
    language = generate_card(str(paload["ngs"]),int(paload["occasion"]),int(paload["num"]))
    return Response(content=language,media="image/png")