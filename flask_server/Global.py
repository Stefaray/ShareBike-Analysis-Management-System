from enum import Enum
from flask import request, Blueprint
class Identity(Enum):
    admin=0
    ordinary=1

class BikeStatus(Enum):
    Riding=0
    Idle=1

loginBlueprint = Blueprint('Login', __name__,url_prefix="/login")
orderBlueprint = Blueprint('order', __name__,url_prefix="/order")
userBlueprint = Blueprint('user', __name__,url_prefix="/user")
dataBlueprint = Blueprint('data', __name__,url_prefix="/data")