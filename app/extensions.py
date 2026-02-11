from flask_pymongo import PyMongo
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

mongo = PyMongo()
api = Api()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(key_func=get_remote_address)
