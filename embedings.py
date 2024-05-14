import os
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key

# Set OpenAI API key
api_key = OpenAI(
  api_key=os.getenv('OPENAI_API_KEY'),  # this is also the default, it can be omitted
)


# # Connect to MongoDB and fetch activities
# def fetch_activities():
#     mongo_uri = os.getenv('MONGO_URI')
#     client = MongoClient(mongo_uri)
#     db = client['ecotourism']
#     collection = db['activities']
#     return list(collection.find())

# # Generate embeddings using OpenAI's text-embedding-ada-002 model
# def generate_embedding(text):
#     response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
#     return response['data'][0]['embedding']

# # Generate and store embeddings for activities
# def generate_and_store_embeddings_activities():
#     activities = fetch_activities()
#     mongo_uri = os.getenv('MONGO_URI')
#     client = MongoClient(mongo_uri)
#     collection = client['ecotourism']['activities']

#     for activity in activities:
#         if 'embedding' not in activity:
#             embedding = generate_embedding(activity['Description'])
#             collection.update_one(
#                 {'_id': activity['_id']},
#                 {'$set': {'embedding': embedding}}
#             )
#     print("Embeddings generated and stored successfully.")



# Connect to MongoDB and fetch regions
def fetch_regions():
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['eco-activities-mu']
    collection = db['regions']
    return list(collection.find())

# Connect to MongoDB and fetch distances
def fetch_distance_matrix():
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['eco-activities-mu']
    collection = db['distance_matrix']
    return collection.find_one()

# Generate embeddings using OpenAI's text-embedding-ada-002 model
def generate_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response =  api_key.embeddings.create(input = [text], model=model).data[0].embedding
    # response = api_key.embeddings.create(input=[text], model="text-embedding-ada-002")
    return response

# Generate and store embeddings for regions and distances
def generate_and_store_embeddings():
    regions = fetch_regions()
    distance_matrix_data = fetch_distance_matrix()
    num_regions = len(regions)

    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    region_collection = client['eco-activities-mu']['regions']
    distance_collection = client['eco-activities-mu']['distances']

    # Generate embeddings for regions
    for region in regions:
        if 'embedding' not in region:
            description = f"{region['Name']} located at GPS coordinates {region['GPS']}"
            embedding = generate_embedding(description)
            region_collection.update_one(
                {'_id': region['_id']},
                {'$set': {'embedding': embedding}}
            )

    # Extract the distance matrix
    distance_matrix = distance_matrix_data["matrix"]

    # Check if the distance matrix matches the number of regions
    if len(distance_matrix) != num_regions or any(len(row) != num_regions for row in distance_matrix):
        raise ValueError("The number of regions does not match the dimensions of the distance matrix.")

    # Generate embeddings for distances
    distance_descriptions = []
    for i, row in enumerate(distance_matrix):
        for j, distance in enumerate(row):
            if i != j:
                description = f"Distance from {regions[i]['Name']} to {regions[j]['Name']} is {distance} minutes"
                embedding = generate_embedding(description)
                distance_descriptions.append({
                    "region_from": regions[i]['ID'],
                    "region_to": regions[j]['ID'],
                    "distance": distance,
                    "embedding": embedding
                })

    # Store the distance matrix embeddings
    distance_collection.insert_many(distance_descriptions)
    print("Region and distance embeddings generated and stored successfully.")

if __name__ == "__main__":
    generate_and_store_embeddings()