#!/usr/bin/python3
"""Defines the Place class"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represents a place entity

    Attributes:
        city_id (str): 
            The ID of the city where the place is located
        user_id (str): 
            The ID of the user who owns the place
        name (str):
            The name of the place
        description (str): 
            The description of the place
        number_of_rooms (int):
            The number of rooms available in the place
        number_of_bathrooms (int): 
            The number of bathrooms available in the place
        max_guests (int): 
            The maximum number of guests the place can accommodate
        price_per_night (int):
            The price per night for staying at the place
        latitude (float): 
            The latitude coordinate of the place
        longitude (float):
            The longitude coordinate of the place
        amenity_ids (list):
            A list of amenity IDs available in the place
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
