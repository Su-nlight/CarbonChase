import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, status, HTTPException
import profile
from models import Token, PredictionRequest, columns
from jose import jwt, JWTError, ExpiredSignatureError
import os
from database import Database
import auth
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import openai
from openai import OpenAI

loaded_model = joblib.load('final_model_v1.pkl')
app = FastAPI()
app.include_router(auth.router)
app.include_router(profile.router)

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
openai.api_key = OPENAI_API_KEY
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.aimlapi.com",
)


def generate_recommendation(user_data, pred):
    """
    Generates personalized recommendations based on user's carbon emission data.

    Args:
      user_data: A dictionary containing user's carbon emission data.

    Returns:
      A string containing the AI's personalized recommendation.
    """

    response = client.chat.completions.create(
        model="gpt-4",  # Set the default model to gpt-4
        messages=[
            {
                "role": "system",
                "content": "you are the AI assitant that works at CarbonChase where we offer people to track their carbon footprints and reward them for reducing them to save earth, your job is to suggest users that how can they improve in reducing their carbon emissions based on which factors have contributed the most in user's carbon emission json data. you have the knowledge of all the world and how to save it, you know how to protect earth from global warming and climate changes and you are an expert at providing serious and good personalised suggestions to people that help us reduce their carbon emissions. you always give medium length responses to user while promoting our company CarbonCounter.",
            },
            {
                "role": "user",
                "content": f"Hey, check out this dataframe {user_data} to see what factors are causing my carbon emissions. My today's emission is {pred}, what should I do?",
            },
        ],
    )

    return response.choices[0].message.content
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/predict", status_code=status.HTTP_200_OK)
async def predict(token: Token, predictionreq: PredictionRequest):
    try:
        decoded_tokn = jwt.decode(token.access_token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    req_field = []
    for i in columns[0:2]:
        req_field.append(i.lower().replace(" ", "_"))
    temp_data = Database.get_user_data(username=decoded_tokn['username'], required_fields=tuple(req_field))
    predictionreq = predictionreq.dict()

    temp = "%s, " * 20
    temp = temp[0:-2]
    fields = ""
    for i in predictionreq.keys():
        fields += ", {}".format(i)
    fields += ", prediction, dated"

    pred_data = [temp_data["body_type"], temp_data["sex"]]
    parameter = [decoded_tokn.get("username")]
    for i in predictionreq.values():
        pred_data.append(i)
        parameter.append(i)
    query = f"insert into predictionrequest (username{fields}) values ({temp});"

    predictionreq["VehicleDailyDistanceKm"] = predictionreq["VehicleDailyDistanceKm"]*30

    user_data = pd.DataFrame(pred_data, columns).T
    prediction = loaded_model.predict(user_data)
    parameter.append(int(prediction[0]))
    parameter.append(datetime.date.today())
    Database.execute_query(query=query, params=parameter)
    recommendation = generate_recommendation(user_data, prediction[0])
    return {"CarbonEmission": prediction[0],"recomendation":recommendation}

