from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, conint


columns=['Body Type', 'Sex', 'Diet', 'How Often Shower', 'Heating Energy Source', 'Transport', 'Vehicle Type',
             'Social Activity', 'Monthly Grocery Bill','Frequency of Traveling by Air', 'Vehicle Monthly Distance Km',
             'Waste Bag Size', 'Waste Bag Weekly Count', 'How Long TV PC Daily Hour', 'How Many New Clothes Monthly',
             'How Long Internet Daily Hour', 'Energy efficiency', 'Recycling', 'Cooking_With']


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    location: Optional[str] = None
    country_code: Optional[str] = None

class UpdateUser(BaseModel):
    email: Optional[str] = None
    location: Optional[str] = None
    country_code: Optional[str] = None
    body_type: Optional[Literal['underweight', 'normal', 'overweight', 'obese']] = None


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    location: str
    country_code: str
    body_type: Literal['underweight', 'normal', 'overweight', 'obese']
    gender: Literal['male', 'female']


class PredictionRequest(BaseModel):
    Diet: Literal['omnivore', 'vegetarian', 'pescatarian', 'vegan']
    HowOftenShower: Literal['daily', 'less frequently', 'more frequently', 'twice a day']
    HeatingEnergySource: Literal['coal', 'natural gas', 'wood', 'electricity']
    Transport: Literal['public', 'walk/bicycle', 'private']
    VehicleType: Literal['petrol', 'diesel', 'hybrid', 'lpg', 'electric']
    SocialActivity: Literal['often', 'never', 'sometimes']
    MonthlyGroceryBill: conint(ge=50, le=299)  # US dollar
    FrequencyOfTravelingWithAir: Literal['frequently', 'rarely', 'never', 'very frequently']
    VehicleDailyDistanceKm: conint(ge=0, le=333)
    WasteBagSize: Literal['large', 'extra large', 'small', 'medium']
    WasteBagWeeklyCount: conint(ge=1, le=7)
    HowLongTVPCDailyHour: conint(ge=0, le=24)
    HowManyNewClothesMonthly: conint(ge=0, le=50)
    HowLongInternetDailyHour: conint(ge=0, le=24)
    EnergyEfficiency: Literal['No', 'Sometimes', 'Yes']
    Recycling: str # ['plastic','glass','metal']
    Cooking_With: str

class UserData(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    gender:Literal['male', 'female']
    body_type:Literal['underweight', 'normal', 'overweight', 'obese']
    location:str
    country_code:str

class ArticleSubmitRequest(BaseModel):
    title: str
    content: str
