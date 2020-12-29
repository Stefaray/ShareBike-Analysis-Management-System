from datetime import *
from  random import *
from model.user import User
from utils import *

def getRandomName():
    len=10
    name=""
    base1='A'
    base2='a'
    for i in range(len):
        if (randint(1, 2) % 2):
            name+=chr(ord(base1)+randint(0,25))
        else:
            name += chr(ord(base2) + randint(0, 25))
    return name

def genPhone():
    len=10
    phone="1"
    for i in range(len):
        phone+=str(randint(0,9))
    return phone

def genEmail():
    return getRandomName()+"@email.com"


from Global import *



import math

def strfy(a):
    return '\''+a+'\''


def PinChou(num):
    base=''
    if(len(str(num))==1):
        base='0'+str(num)
    else:
        base=str(num)
    return base+":00:00"

import json

list=[
    {
      "NorthEast_location" :{"x":121.5,"y":31.4},
       "SouthWest_location":{"x":121.3,"y":31.5}
    },
    {
        "NorthEast_location" :{"x":121.8,"y":31.1},
        "SouthWest_location":{"x":121.5,"y":31.3}
    },
]

print(json.dumps(list))
