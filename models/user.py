#!/usr/bin/python3
"""
user module
with User class
"""

from models.base_model import BaseModel
import json


class User(BaseModel):
    '''
    base model class
    '''

    email = ""
    password = ""
    first_name = ""
    last_name = ""
