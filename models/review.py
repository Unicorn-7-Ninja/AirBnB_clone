#!/usr/bin/python3
"""Defines the Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a review entity &

    Attributes:
        place_id (str): The ID of the place being reviewed
        user_id (str): The ID of the user who created the review
        review_text (str): The text content of the review
    """

    place_id = ""
    user_id = ""
    text = ""
