from decouple import config
import jwt

JWT_SECRET_KEY = config('JWT_SECRET_KEY')


def create_jwt(email):

    return jwt.encode({'email': email}, JWT_SECRET_KEY, algorithm="HS256")
