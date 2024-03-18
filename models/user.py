#!/usr/bin/python3
"""Defines the User class"""

from models.base_model import BaseModel


class User(BaseModel):
    """Represents a user entity & Attributes:
        user_email (str): The email address of the user
        user_password (str): The password of the user account
        user_first_name (str): The first name of the user
        user_last_name (str): The last name of the user
    """  
    email = ""
    password = ""
    first_name = ""
    last_name = ""
