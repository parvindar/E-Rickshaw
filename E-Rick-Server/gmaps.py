import googlemaps
import json
from datetime import datetime

# Google Maps API 

gmaps = googlemaps.Client(key='AIzaSyDDxYfHvtgh7L-TUAMz2Wnn479AB2ZwOns')


# Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# print("geocode",geocode_result)

# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# print("reverse geo" , reverse_geocode_result)

# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions(40.714224, -73.961452,
#                                      mode="transit",
#                                      departure_time=now)


# Requires geo-coordinates(latitude/longitude) of origin and destination
def get_distance_info(origin_latitude,origin_longitude,destination_latitude,destination_longitude):
	# origin_latitude = 26.186216
	# origin_longitude = 91.689683
	# destination_latitude = 26.189109 
	# destination_longitude = 91.695791
	distance = gmaps.distance_matrix([str(origin_latitude) + " " + str(origin_longitude)], [str(destination_latitude) + " " + str(destination_longitude)], mode='driving')['rows'][0]['elements'][0]
	return distance

def get_distance_val(origin_latitude,origin_longitude,destination_latitude,destination_longitude):
	# origin_latitude = 26.186216
	# origin_longitude = 91.689683
	# destination_latitude = 26.189109 
	# destination_longitude = 91.695791
	distance = gmaps.distance_matrix([str(origin_latitude) + " " + str(origin_longitude)], [str(destination_latitude) + " " + str(destination_longitude)], mode='driving')['rows'][0]['elements'][0]
	val = distance["distance"]["value"]
	return val

def get_duration_val(origin_latitude,origin_longitude,destination_latitude,destination_longitude):
	# origin_latitude = 26.186216
	# origin_longitude = 91.689683
	# destination_latitude = 26.189109 
	# destination_longitude = 91.695791

	distance = gmaps.distance_matrix([str(origin_latitude) + " " + str(origin_longitude)], [str(destination_latitude) + " " + str(destination_longitude)], mode='driving')['rows'][0]['elements'][0]
	try:
		val = distance["duration"]["value"]
	except Exception as e:
		val = -1
		print(e)
	return val



# origin_latitude = 26.186216
# origin_longitude = 91.689683
# destination_latitude = 26.189109 
# destination_longitude = 91.695791

# val = get_duration_val(origin_latitude,origin_longitude,destination_latitude,destination_longitude)
# # dis = get_distance_info(origin_latitude,origin_longitude,destination_latitude,destination_longitude)

# # print(dis)
# print(val)

