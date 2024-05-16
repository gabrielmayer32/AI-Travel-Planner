import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi

# Load environment variables from .env file
load_dotenv()
uri = "mongodb+srv://gabriel0mayer:AeJootCuwjjnTKge@cluster0.1m4jiuy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
# MongoDB Atlas connection string
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
db = client['eco-activities-mu']  # Replace with your database name
collection = db['hotels']  # Replace with your collection name

activities = [{'ID': 1, 'Name': 'Salt of palmar ', 'Tags': 'Hotel, Eco-Friendly\n', 'Dietary': '', 'Location': '', 'GPS': '', 'Description': 'SALT of Palmar is a small, adults-only boutique hotel on the east coast of Mauritius. Combining sustainability with luxury, SALT features minimalist but elegant decor, its own bakery, and fresh roasted coffee available 24/7. Guests can enjoy a library, craft workshops, a rooftop bar, and a pool bar with locally inspired cocktails. The hotel prioritizes local produce, eliminates single-use plastics, and empowers local communities through job opportunities and cultural experiences.', 'Duration': '', 'Region ID': 12}, {'ID': 2, 'Name': 'Zilwa attitude', 'Tags': 'Hotel, Eco-Friendly\n', 'Dietary': '', 'Location': '', 'GPS': '', 'Description': 'Zilwa Attitude, part of the Attitude hotel collection, offers 3* and 4* accommodations with an authentic Mauritian atmosphere. Known for its happy and empowered staff, the hotel creates a positive and welcoming vibe for guests. The Creole-style decor, locally inspired Taba-J street food stalls, and beachfront locations make it a standout choice. The hotel emphasizes sustainability by reducing water and energy consumption, banning single-use plastics, and sourcing local ingredients. Guests receive reusable water bottles, and spa products are cruelty-free and plant-based. The Marine Discovery Centre and the Green Attitude Foundation further support local environmental and sustainable initiatives.', 'Duration': '', 'Region ID': 7}, {'ID': 3, 'Name': 'Otentic Eco Tent Experience\n', 'Tags': 'Lodge, Eco-Friendly\n', 'Dietary': '', 'Location': '', 'GPS': '', 'Description': 'Located in the village of Deux Frères on the east coast of Mauritius, Otentic Eco Tent Experience offers a unique, outdoorsy stay perfect for disconnecting from the world. Set along the Grand River South East near the GRSE waterfall, the eco tents provide protection from the elements with their canvas and fly-sheet structure. Guests can enjoy a pool with river views, outdoor lounge, dining area, and trips to Iles aux Cerfs, as well as hiking and snorkeling. Built from recycled materials and wood, the eco lodge features zero-impact activities like kayaking, paddleboarding, and biking. Locally sourced produce, a vegetable garden, rainwater harvesting, and solar energy underscore its commitment to sustainability.', 'Duration': '', 'Region ID': 12}, {'ID': 4, 'Name': 'Lux Le Morne', 'Tags': 'Hotel, Luxurious Eco-sonscious', 'Dietary': '', 'Location': '', 'GPS': '', 'Description': 'Lux Le Morne is a luxurious 5-star resort set against the iconic Le Morne Brabant mountain and a stunning turquoise lagoon. Awarded both the Travelife and Green Globe sustainability certifications, the resort is dedicated to social and environmental responsibility. Guests enjoy personalized services, including pre-ordered snacks and drinks, a customizable picnic basket, and pet-friendly accommodations. Unique features like an ocean-view tree house, tree swing, hanging beds, and a hammock in the lagoon enhance the guest experience. The resort strives for carbon neutrality, uses energy-efficient practices, bottles its own water, employs chemical-free cleaning agents, and recycles extensively. Their zero food waste policy supports local children and sustainable practices.', 'Duration': '', 'Region ID': 3}, {'ID': 5, 'Name': 'Bubble Lodge', 'Tags': 'Lodge, Unique Experience, Nature Immersion', 'Dietary': '', 'Location': '', 'GPS': '', 'Description': 'Bubble Lodge at Bois Chéri offers a unique stay in transparent bubbles surrounded by tea plantations. Located near a crater lake, each lodge provides utmost privacy and luxury with dedicated staff and air renewal every 10 minutes. Ideal for a digital detox, the rustic yet elegant decor lets guests stargaze and wake up to the sunrise while enjoying nature without the hassle of mosquitoes. Free activities include hiking, kayaking, stand-up paddling, and tea tasting. Eco-friendly features include lodges made from renewable materials, no carbon footprint, dry ecological toilets, and providing bikes, kayaks, and SUPs for exploring the area sustainably.', 'Duration': '', 'Region ID': 12}]



# # Insert activities into the collection
collection.insert_many(activities)

print("Activities added to MongoDB successfully.")


# regions = [
#     {"ID": 1, "Name": "Center", "GPS": "57.5228363565601,-20.313123939641322"},
#     {"ID": 2, "Name": "West", "GPS": "57.377418619655636,-20.364101328996437"},
#     {"ID": 3, "Name": "South-West", "GPS": "57.34673216332586,-20.447948737766215"},
#     {"ID": 4, "Name": "South", "GPS": "57.517002034627616,-20.521670843611272"},
#     {"ID": 5, "Name": "South-East", "GPS": "57.62298050446764,-20.48461472237721"},
#     {"ID": 6, "Name": "North-East", "GPS": "57.69663791659995,-20.083024454732765"},
#     {"ID": 7, "Name": "North", "GPS": "57.62097562565946,-19.973021799643004"},
#     {"ID": 8, "Name": "North-West", "GPS": "57.51990847424628,-20.06383142599121"},
#     {"ID": 9, "Name": "Flic en Flac", "GPS": "57.372788953790746,-20.26915852990059"},
#     {"ID": 10, "Name": "Chamarel", "GPS": "57.39123154281593,-20.441256084660075"},
#     {"ID": 11, "Name": "Bel Ombre", "GPS": "57.42433952659329,-20.510467796326896"},
#     {"ID": 12, "Name": "East", "GPS": "57.77987327922487,-20.30565997871869"},
#     {"ID": 13, "Name": "Port-Louis", "GPS": "57.5063932531739,-20.158594115708112"},
#     {"ID": 14, "Name": "Center-East", "GPS": "57.645661729084615,-20.233289171329247"}
# ]


# region_collection = db['regions']
# region_collection.insert_many(regions)

# print("Regions added to MongoDB successfully.")


# distance_matrix = {
#     "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
#     "matrix": [
#         [0, 34, 43, 32, 22, 45, 44, 33, 28, 36, 38, 43, 23, 26],
#         [34, 0, 13, 39, 55, 61, 60, 49, 20, 15, 27, 75, 36, 50],
#         [43, 12, 0, 26, 42, 72, 71, 60, 31, 10, 14, 73, 47, 61],
#         [32, 39, 26, 0, 17, 76, 76, 65, 57, 28, 11, 51, 54, 55],
#         [22, 55, 42, 17, 0, 66, 65, 55, 49, 43, 26, 35, 44, 45],
#         [45, 61, 72, 76, 66, 0, 20, 26, 55, 74, 79, 38, 25, 29],
#         [44, 60, 71, 76, 65, 20, 0, 18, 54, 74, 78, 57, 25, 43],
#         [33, 49, 60, 65, 55, 26, 18, 0, 44, 63, 68, 57, 14, 32],
#         [28, 20, 31, 57, 48, 54, 53, 43, 0, 34, 46, 68, 29, 43],
#         [36, 15, 10, 28, 43, 74, 73, 62, 34, 0, 16, 67, 49, 62],
#         [38, 27, 14, 11, 27, 81, 81, 70, 46, 16, 0, 61, 57, 64],
#         [43, 75, 73, 51, 35, 38, 57, 57, 68, 67, 61, 0, 55, 27],
#         [23, 36, 47, 54, 44, 26, 25, 15, 30, 50, 58, 56, 0, 31],
#         [26, 50, 61, 55, 45, 29, 43, 32, 43, 62, 64, 27, 31, 0]
#     ]
# }


# distance_collection = db['distance_matrix']
# distance_collection.insert_one(distance_matrix)

# print("Distance matrix added to MongoDB successfully.")
