#!/usr/bin/python3
"""
review module
with Review class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Inherits from BaseModel
    """
    place_id = ""
    user_id = ""
    text = ""
