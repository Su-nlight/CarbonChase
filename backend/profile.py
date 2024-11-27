from __future__ import annotations
from database import Database, get_total_user_data, chk_username
import os
from fastapi import APIRouter, HTTPException
from starlette import status
from models import Token
from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
from models import UpdateUser, UserData
from mysql.connector import Error

router = APIRouter(
    prefix='/me',
    tags=['profile']
)


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

@router.post("/me", status_code=status.HTTP_200_OK)
async def profile(token: Token):
    try:
        # Decode the JWT token
        decoded_tokn = jwt.decode(token.access_token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user_data= get_total_user_data(decoded_tokn['username'])
    temp_data= UserData(email=user_data[0],username=user_data[1],first_name=user_data[2],last_name=user_data[3],gender=user_data[4],
                        body_type=user_data[5],location=user_data[6],country_code=user_data[7]).dict()
    return {"message": "user data found","data":temp_data}


@router.put("/me/update")
async def update_user(token: Token, user_update: UpdateUser):
    try:
        # Decode the JWT token
        decoded_tokn = jwt.decode(token.access_token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    try:
        # Check if the username exists
        check = chk_username(decoded_tokn['username'])
        if not check:
            raise HTTPException(status_code=404, detail="User not found")

        # Prepare the update fields from the provided data
        update_fields = {k: v for k, v in user_update.dict(exclude_unset=True).items()}

        if update_fields:
            # Special handling for email update
            if 'email' in update_fields:
                Database.execute_query("UPDATE users SET email = %s WHERE username = %s", (update_fields['email'], decoded_tokn['username']))
                del update_fields['email']

            # Create the SET clause dynamically based on provided fields
            set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
            update_query = f"UPDATE user_data SET {set_clause} WHERE username = %s"

            # Combine the parameters and execute the query
            parameters = list(update_fields.values()) + [decoded_tokn['username']]
            Database.execute_query(update_query, tuple(parameters))

            # Fetch the updated data
            Database.execute_query("SELECT * FROM user_data WHERE username = %s", (decoded_tokn['username'],))
            user_data= get_total_user_data(decoded_tokn['username'])
            temp_data = UserData(email=user_data[0], username=user_data[1], first_name=user_data[2],
                                 last_name=user_data[3], gender=user_data[4],
                                 body_type=user_data[5], location=user_data[6], country_code=user_data[7]).dict()

            return {"message": "User data updated successfully", "updated_data": temp_data}
        else:
            return {"message": "No fields to update"}

    except Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating user data")