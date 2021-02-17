import requests
import json
import random
import emoji
import time

OFFICE = '-23.5888644,-46.680577'	# Your office coordinates
RADIUS = '400' 	# Radius you're willing to walk to the restaurant
KEY = ''	# Your Google API key

rng = random.SystemRandom()

r = requests.post(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json\
?location={OFFICE}&radius={RADIUS}&type=restaurant&opennow=true&key={KEY}')

s = r.json()

restaurants = s['results']

while ('next_page_token' in s):
	PAGETOKEN = s['next_page_token']
	s['status'] = ''	# Tokens take a while to be valid so keep trying until the return status is OK

	while (s['status'] != 'OK'):
		r = requests.post(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json\
?pagetoken={PAGETOKEN}&key={KEY}')

		s = r.json()

	restaurants.extend(s['results'])

print(len(restaurants))

chosen_restaurant = restaurants[rng.randint(0, len(restaurants) - 1)]

print(chosen_restaurant['name'])
if ('price_level' in chosen_restaurant):
	print('$'*chosen_restaurant['price_level'])
if ('rating' in chosen_restaurant):
	print(emoji.emojize(':star:', use_aliases=True)*int(chosen_restaurant['rating']) + ' ' + str(chosen_restaurant['rating']))

print(chosen_restaurant['geometry']['location']['lat'])
print(chosen_restaurant['geometry']['location']['lng'])