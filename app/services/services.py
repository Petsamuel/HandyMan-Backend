
from database import get_db
from models import models
import geopy.distance

def find_nearby_handymen(request, db):
    handymen = db.query(models.Handyman).all()
    nearby_handymen = []
    user_location = (request.latitude, request.longitude)
    
    for handyman in handymen:
        handyman_location = (handyman.latitude, handyman.longitude)
        distance = geopy.distance.distance(user_location, handyman_location).km
        if distance <= 10:  # Example: 10 km radius
            nearby_handymen.append({
                "handyman_id": handyman.id,
                "distance": distance,
                "rating": handyman.rating,  # Assuming rating is a field in Handyman
                "phone":handyman.phone
            })

    nearby_handymen.sort(key=lambda x: (x["distance"], -x["rating"]))
    return nearby_handymen
