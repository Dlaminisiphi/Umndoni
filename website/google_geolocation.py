# Import necessary libraries
import googlemaps
from geopy.distance import geodesic
import os

# Fetch the Google Maps API key from the environment variable
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

# Google Maps Client instance using the API key
gmaps = googlemaps.Client(key=google_maps_api_key)

# Import additional libraries for geocoding
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

#  Google Maps Client instance with a different API key (replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual key)
gmaps = googlemaps.Client(key=google_maps_api_key)

# Function to get coordinates (latitude, longitude) from an user address using Nominatim geocoding
def get_coordinates_from_address(address):
    geolocator = Nominatim(user_agent="geopy")  
    
    try:
        location = geolocator.geocode(address)  
        if location:
            return location.latitude, location.longitude  
    except GeocoderTimedOut:
        pass  
    
    return None  

# Function to check if user address is within Umndoni Municipality
def is_within_distance(coord1, coord2, distance_km):
    if coord1 and coord2:
        return geodesic(coord1, coord2).kilometers <= distance_km  
    return False  
