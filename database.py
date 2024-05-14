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
collection = db['activities']  # Replace with your collection name

activities = [
    {"ID": 1, "Name": "Safari Adventures at Casela Nature Parks", "Tags": "Wildlife, quad, biking", "Dietary": "Any", "Location": "Cascavelle", "GPS": "57.40401659984193, -20.290822520340747", "Description": "A scenic mountain trail offering panoramic views.", "Duration": "4 hours", "Region ID": 2},
    {"ID": 2, "Name": "Rivulet Terre Rouge Estuary Bird Sanctuary", "Tags": "Birdwatching, conservation", "Dietary": "Vegetarian", "Location": "Port Louis, Mauritius", "GPS": "57.50305012462502,-20.141135663039513", "Description": "Stay in an eco-friendly lodge with sustainable practices.", "Duration": "1 hour", "Region ID": 8},
    {"ID": 3, "Name": "Bel Ombre Nature Reserve", "Tags": "Hiking, quad, guided tour", "Dietary": "", "Location": "Bel Ombre", "GPS": "57.44063292463474,-20.5007388447369", "Description": "", "Duration": "4 hours", "Region ID": 3},
    {"ID": 4, "Name": "Explorers Mauritius", "Tags": "Hiking", "Dietary": "", "Location": "", "GPS": "57.342712022859374,-20.44599006947597", "Description": "", "Duration": "4 hours", "Region ID": 10},
    {"ID": 5, "Name": "Vallée des Couleurs Nature Park", "Tags": "Nature park, quad, biking", "Dietary": "", "Location": "", "GPS": "57.48512435224131,-20.45734257198024", "Description": "", "Duration": "2 hours", "Region ID": 10},
    {"ID": 6, "Name": "La Vanille Nature Park", "Tags": "Nature park", "Dietary": "", "Location": "", "GPS": "57.56385135354587,-20.4992840416064", "Description": "", "Duration": "2 hours", "Region ID": 5},
    {"ID": 7, "Name": "World of Seashells Museum", "Tags": "Museum", "Dietary": "", "Location": "Bel Ombre", "GPS": "57.412948330258935,-20.505400998259997", "Description": "", "Duration": "1 hour", "Region ID": ""},
    {"ID": 8, "Name": "Le Parc Loisirs de Gros Cailloux", "Tags": "Leisure park", "Dietary": "", "Location": "", "GPS": "57.43389838662021,-20.212688191452337", "Description": "", "Duration": "4 hours", "Region ID": 2},
    {"ID": 9, "Name": "Ebony Forest Discovery Tour", "Tags": "Birdwatching, hiking", "Dietary": "", "Location": "", "GPS": "57.37387709641916,-20.43747662521102", "Description": "", "Duration": "3 hours", "Region ID": 10},
    {"ID": 10, "Name": "National Botanical Garden in Mauritius", "Tags": "Garden visit", "Dietary": "", "Location": "Pamplemousses", "GPS": "57.58063683264565,-20.104541404788456", "Description": "", "Duration": "1 hour", "Region ID": 8},
    {"ID": 11, "Name": "St Felix Beach", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.46546886059799,-20.508867023571405", "Description": "", "Duration": "2 hours", "Region ID": 4},
    {"ID": 12, "Name": "Flic en flac Beach", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.36278382556547,-20.28883901542467", "Description": "", "Duration": "2 hours", "Region ID": 9},
    {"ID": 13, "Name": "Tamarin Beach", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.377096414408165,-20.3269160116297", "Description": "Atypical places, volcanic sand, great scenery with the mountains behind", "Duration": "2 hours", "Region ID": 2},
    {"ID": 14, "Name": "Belle Mare Plage", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.77109956278965,-20.168930256638877", "Description": "A stunning 6-mile stretch of talcum-white sand on the northeast coast, ideal for water sports and relaxation", "Duration": "2 hours", "Region ID": 12},
    {"ID": 15, "Name": "Ile aux Cerf", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.807553455093284,-20.274051301682327", "Description": "Famous for its white sandy beaches, this island off the east coast also offers an 18-hole golf course and various water activities", "Duration": "2 hours", "Region ID": 12},
    {"ID": 16, "Name": "Le Morne", "Tags": "Beach, kite", "Dietary": "", "Location": "", "GPS": "57.3126770707331,-20.451864200163712", "Description": "A 2.5-mile beach with pristine white sand and a dramatic backdrop of the Le Morne Brabant peak, popular with kitesurfers", "Duration": "2 hours", "Region ID": 3},
    {"ID": 17, "Name": "Blue Bay", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.716363551537114,-20.44385240836454", "Description": "A rugged beach on the southeast coast with clear waters great for swimming and snorkeling, especially during the week when it's less crowded", "Duration": "2 hours", "Region ID": 5},
    {"ID": 18, "Name": "La Cuvette Beach", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.578073083131706,-20.007111017153267", "Description": "A small but beautiful beach near Grand Bay, known for its tranquil atmosphere and basin-like effect in the water", "Duration": "2 hours", "Region ID": 8},
    {"ID": 19, "Name": "Trou aux Biches", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.5442447373683,-20.035695755184545", "Description": "Located in the north, this beach has unbelievably blue waters and white sands, with a relaxed atmosphere", "Duration": "2 hours", "Region ID": 8},
    {"ID": 20, "Name": "Mont Choisy", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.55244347703669,-20.00330279063435", "Description": "The longest beach in the northern region, with soft white sand and warm turquoise waters, never too crowded", "Duration": "2 hours", "Region ID": 8},
    {"ID": 21, "Name": "Poste Lafayette", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.756899934438145,-20.127726734163822", "Description": "A beach in the east known for its casuarina trees providing shade, and opportunities for snorkeling and diving", "Duration": "2 hours", "Region ID": 12},
    {"ID": 22, "Name": "Bain Boeuf", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.604974354233356,-19.986078484740517", "Description": "A beach in the north with a relaxed vibe, good for swimming and snorkeling", "Duration": "2 hours", "Region ID": 7},
    {"ID": 23, "Name": "Riambel", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.481864141363914,-20.518974072805108", "Description": "A long beach in the south with black sand and a rugged, windswept feel", "Duration": "2 hours", "Region ID": 4},
    {"ID": 24, "Name": "Gris Gris", "Tags": "Beach", "Dietary": "", "Location": "", "GPS": "57.53302045903951,-20.52428940294336", "Description": "A scenic beach in the south with dramatic cliffs and strong waves, not suitable for swimming", "Duration": "2 hours", "Region ID": 4},
    {"ID": 25, "Name": "Anse la Raie", "Tags": "Beach, kite", "Dietary": "", "Location": "", "GPS": "57.632345007428825,-19.99058698683819", "Description": "A beach in the north with a shallow lagoon, popular for kitesurfing and windsurfing", "Duration": "2 hours", "Region ID": 7},
    {"ID": 26, "Name": "Palmar", "Tags": "Beach, kite", "Dietary": "", "Location": "", "GPS": "57.79231980423732,-20.210155762292388", "Description": "A beach in the east with fine white sand and a relaxed atmosphere, good for swimming and snorkeling", "Duration": "2 hours", "Region ID": 12},
    {"ID": 27, "Name": "Aapravasi Ghat", "Tags": "Cultural site", "Dietary": "", "Location": "Port Louis", "GPS": "57.502966310312566,-20.158508956068232", "Description": "A UNESCO World Heritage Site, this historic site marks the arrival of indentured laborers from India and other parts of Asia in the 19th century. It features the ruins of the structures that shaped the complex, used by indentured laborers under British colonial rule", "Duration": "1 hour", "Region ID": 13},
    {"ID": 28, "Name": "Grand Bassin (Ganga Talao)", "Tags": "Cultural site", "Dietary": "", "Location": "", "GPS": "57.491723359133225,-20.41792867497075", "Description": "A sacred Hindu site, Grand Bassin is a dormant volcano nestled in the heart of lush nature, where you can recharge your batteries. It's a high place of pilgrimage for the Hindu", "Duration": "1 hour", "Region ID": 1},
    {"ID": 29, "Name": "Maheshwarnath Mandir", "Tags": "Cultural site", "Dietary": "", "Location": "", "GPS": "57.504684063273224,-20.32823577786467", "Description": "A Hindu temple worth visiting for its architectural beauty and historical significance", "Duration": "30 minutes", "Region ID": 13},
    {"ID": 30, "Name": "Jummah Mosque", "Tags": "Cultural site", "Dietary": "", "Location": "", "GPS": "57.50646512519154,-20.161117080944983", "Description": "A beautiful mosque in the capital city, known for its architectural style and historical significance", "Duration": "30 minutes", "Region ID": 13},
    {"ID": 31, "Name": "Kwan Tee Pagoda", "Tags": "Cultural site", "Dietary": "", "Location": "", "GPS": "57.49200497334183,-20.161661438445133", "Description": "A Chinese temple in the capital city, known for its architectural beauty and historical significance", "Duration": "30 minutes", "Region ID": 14},
    {"ID": 32, "Name": "Saint Francis of Assisi Church", "Tags": "Cultural site", "Dietary": "", "Location": "", "GPS": "57.51423063532578,-20.154828318044146", "Description": "The oldest still-standing church in Mauritius, built in the 18th century.", "Duration": "30 minutes", "Region ID": 8},
    {"ID": 33, "Name": "Government House", "Tags": "Historical site", "Dietary": "", "Location": "", "GPS": "57.50344115032808,-20.163079866567383", "Description": "A French colonial building built in 1738, now serving as the official residence of the Governor-General of Mauritius", "Duration": "30 minutes", "Region ID": 13},
    {"ID": 34, "Name": "Central Post Office", "Tags": "Historical site", "Dietary": "", "Location": "", "GPS": "57.50161724809972,-20.159877115627136", "Description": "A beautiful building housing the post office, known for its architectural style and historical significance", "Duration": "30 minutes", "Region ID": 13},
    {"ID": 35, "Name": "Vieux Grand Port Historical Route", "Tags": "Historical site, museum", "Dietary": "", "Location": "", "GPS": "57.72196393623412,-20.37414842921838", "Description": "A historical route that houses several historical monuments, including the Dutch landing site", "Duration": "30 minutes", "Region ID": 5},
    {"ID": 36, "Name": "Château de Labourdonnais", "Tags": "Cultural site", "Dietary": "", "Location": "", "GPS": "57.61760336751782,-20.073375370728264", "Description": "A historic château built in the 19th century, now serving as a museum and offering insights into the history of Mauritius", "Duration": "30 minutes", "Region ID": 7},
    {"ID": 37, "Name": "Martello Tower", "Tags": "Cultural site", "Dietary": "", "Location": "", "GPS": "57.36187994878804,-20.354479136817215", "Description": "A historic tower built by the British in the 19th century, now serving as a museum and offering stunning views of the surrounding area", "Duration": "30 minutes", "Region ID": 2},
    {"ID": 38, "Name": "Maison Eureka", "Tags": "Historical site", "Dietary": "", "Location": "", "GPS": "57.49783459423478,-20.217788464498405", "Description": "Maison Eureka is a 19th-century Creole-style house turned museum, offering insights into the colonial life of the time. It features incredible furniture, old maps, and remarkable antiques, providing a glimpse into Mauritius' history", "Duration": "2 hours", "Region ID": 1},
    {"ID": 39, "Name": "Beau Plan Sugar Mill", "Tags": "Historical site", "Dietary": "", "Location": "", "GPS": "57.48149093053592,-20.165065501814528", "Description": "The Sugar Museum and Factory at Beau Plan showcases the history of sugar production in Mauritius, including the island's rum trade, slavery, and the significance of sugar. The tour ends with a sugar tasting experience", "Duration": "2 hours", "Region ID": 8},
    {"ID": 40, "Name": "Le Morne", "Tags": "Historical site", "Dietary": "", "Location": "", "GPS": "57.31662066196576,-20.448925952380087", "Description": "Le Morne Brabant is a UNESCO World Heritage Site commemorating the fight for freedom of slaves in Mauritius. The monument at the foot of the mountain symbolizes the struggle for liberation and freedom", "Duration": ">1 hour", "Region ID": 3},
    {"ID": 41, "Name": "SOS Children Village", "Tags": "Volunteering", "Dietary": "", "Location": "", "GPS": "", "Description": "Here is their email soschild@soscvmauritius.org", "Duration": "", "Region ID": ""},
    {"ID": 42, "Name": "PAWS", "Tags": "Volunteering, animal", "Dietary": "", "Location": "", "GPS": "", "Description": "More info here https://www.pawsmauritius.org/volunteer-with-us/", "Duration": "", "Region ID": ""},
    {"ID": 43, "Name": "Ebony Forest", "Tags": "Volunteering, conservation, wildlife", "Dietary": "", "Location": "", "GPS": "", "Description": "https://www.ebonyforest.com/volunteer/", "Duration": "", "Region ID": ""},
    {"ID": 44, "Name": "Reef Conservation", "Tags": "Volunteering, conservation, sea", "Dietary": "", "Location": "", "GPS": "", "Description": "https://www.reefconservation.mu/support-us/become-a-volunteer/", "Duration": "", "Region ID": ""}
]



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
