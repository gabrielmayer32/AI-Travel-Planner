import streamlit as st
import os
from datetime import date
from pymongo import MongoClient
from dotenv import load_dotenv
import numpy as np
import requests
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

api_key = st.secrets["OPENAI_API_KEY"]

if api_key is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in the secrets.")
else:
    client = OpenAI(api_key=api_key)





# Initialize the application's title and subtitle
st.title('Eco Travel Planner for Your Stay in Mauritius')
st.subheader('Plan your next trip with us')

# User input section in the sidebar
st.sidebar.header('Enter details to generate a travel plan:')
source = st.sidebar.text_input('Where you come from?', 'New York')
date_input = st.sidebar.date_input('Travel Start Date', min_value=date.today())
date = date_input.strftime('%Y-%m-%d')
# budget = st.sidebar.number_input('Budget', min_value=100, value=1000, step=100)
duration = st.sidebar.slider('Duration (days)', 1, 15, 7)

# Currency selector
# currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']  
# selected_currency = st.sidebar.selectbox('Select Currency', currencies)

# Additional user preferences
st.sidebar.subheader('Your Preferences:')
language_preference = st.sidebar.selectbox('Language Preference', ['English', 'Spanish', 'French', 'German', 'Japanese'], index=0)
# interests = st.sidebar.text_input('Interests', 'historical sites, nature')
predefined_interests = [
    'historical sites', 'nature', 'museum', 'hike', 
    'beach', 'wildlife', 'adventure sports', 'local culture', 
    'eco-friendly activities','bird watching', 'botanical gardens', 'cultural sites', 'voluntering'
]

interests = st.sidebar.multiselect('Select Your Interests', predefined_interests, default=['hike', 'museum'])

dietary_restrictions = st.sidebar.text_input('Dietary Restrictions', 'None')
activity_level = st.sidebar.selectbox('Activity Level', ['Low', 'Moderate', 'High'])
specific_interests = st.sidebar.text_input('Specific Interests', 'art museums, hiking trails')
accommodation_preference = st.sidebar.selectbox('Eco-Accommodation Preference', ['Hotel', 'Lodge' ])
travel_style = st.sidebar.selectbox('Travel Style', ['Relaxed', 'Fast-Paced', 'Adventurous', 'Cultural', 'Family-Friendly'])
# must_visit_landmarks = st.sidebar.text_input('Must-Visit Landmarks', 'e.g., Eiffel Tower, Grand Canyon')

# Connect to MongoDB and fetch data

def fetch_data(collection_name):
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client['eco-activities-mu']
    collection = db[collection_name]
    return list(collection.find())

# Generate embeddings using OpenAI's text-embedding-ada-002 model
def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

# Calculate cosine similarity
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Find similar activities based on user preferences
def find_similar_activities(user_preferences, activities, top_n=10):
    # query_description = f"{user_preferences['interests']}, {user_preferences['specific_interests']}"
    query_description = f"{user_preferences['interests']}"
    query_embedding = get_embedding(query_description)

    embeddings = [activity['embedding'] for activity in activities if 'embedding' in activity]
    if not embeddings:
        st.error("No embeddings found for activities")
        return []

    similarities = [cosine_similarity(query_embedding, embedding) for embedding in embeddings]
    if not similarities:
        st.error("No similarities calculated")
        return []

    # Get the indices of the top_n most similar activities
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    return [activities[i] for i in top_indices]

# Calculate optimal route
def calculate_optimal_route(activities, hotels, distances):
    # Combine region IDs from both activities and hotels
    location_regions = []
    for activity in activities:
        try:
            region_id = int(activity['Region ID'])
            location_regions.append(region_id)
        except (ValueError, TypeError):
            continue  # Skip activities with invalid or missing Region ID

    for hotel in hotels:
        try:
            region_id = int(hotel['Region ID'])
            location_regions.append(region_id)
        except (ValueError, TypeError):
            continue  # Skip hotels with invalid or missing Region ID

    if not location_regions:
        raise ValueError("No valid Region ID found in activities or hotels")

    route = []
    visited = set()

    current_region = location_regions[0]
    route.append(current_region)
    visited.add(current_region)

    while len(visited) < len(location_regions):
        next_region = None
        min_distance = float('inf')
        
        for region in location_regions:
            if region not in visited and distances[current_region - 1][region - 1] < min_distance:
                next_region = region
                min_distance = distances[current_region - 1][region - 1]

        if next_region is not None:
            route.append(next_region)
            visited.add(next_region)
            current_region = next_region
        else:
            # If no next region is found, break the loop to prevent infinite loop
            print("No more unvisited regions with valid distances found. Exiting loop.")
            break

    return route


def find_accommodations(user_preferences, accommodations, top_n=3):
    # Filter accommodations based on user preferences
    query_description = " ".join(user_preferences['interests'])
    query_embedding = get_embedding(query_description)
    print(user_preferences['accommodation_preference'])
    
    filtered_accommodations = [
        acc for acc in accommodations
        if any(tag in user_preferences['accommodation_preference'] for tag in acc['Tags'])
    ]
    
    if not filtered_accommodations:
        st.error("No accommodations found matching the criteria")
        return []

    # Calculate similarities using embeddings if available
    if 'embedding' in filtered_accommodations[0]:
        accommodations_embeddings = [acc['embedding'] for acc in filtered_accommodations]
        similarities = [cosine_similarity(query_embedding, embedding) for embedding in accommodations_embeddings]
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        return [filtered_accommodations[i] for i in top_indices]
    else:
        # Sort based on other criteria like ratings if embeddings are not available
        sorted_accommodations = sorted(filtered_accommodations, key=lambda x: x.get('rating', 0), reverse=True)
        return sorted_accommodations[:top_n]




def add_conclusion():
    st.header("Be Aware of Local Rules and Guidelines")
    st.write("""
    It's important to familiarize yourself with local rules and regulations to avoid endangering local wildlife, marine life, or the environment.
    """)

    st.subheader("Dolphin and Whale Watching")
    st.write("""
    If dolphin and whale watching is on your wishlist, there are specific rules to follow to ensure the safety of both you and the marine life. According to the Tourism Authority (Dolphin and Whale Watching) Regulations 2012:
    
    - **Swimming Prohibition:** It is prohibited to swim, dive, or snorkel with whales in Mauritius.
    - **No Feeding:** You cannot feed a dolphin or whale, or throw food or any other object, substance, or matter near or around a dolphin or whale.
    - **Licensed Providers:** You must travel with a licensed whale and dolphin-watching provider.
    - **Approach Guidelines:** Pleasure crafts can only approach whales and dolphins from the side, must follow a parallel course, and operate at a no-wake speed.
    - **No Touching:** You cannot touch, or attempt to touch, a dolphin or whale.
    - **Noise Prohibition:** You cannot make noise to attract their attention or circle around them.
    - **Swimming Briefing:** If swimming with dolphins, you must be briefed on sound techniques related to calm and silent swimming. No more than three swimmers (including a designated lifesaver) can enter, dive, or snorkel simultaneously in the sea.
    
    For full details, refer to the Tourism Authority (Dolphin and Whale Watching) Regulations 2012.
    """)

    st.subheader("Be Aware of the Marine Environment")
    st.write("""
    Our marine environment is very delicate. Here are some tips to help preserve it for future generations:

    - **Do Not Touch:** Do not touch marine organisms. Touching coral will kill it, and other organisms can be venomous.
    - **Avoid Walking on Corals:** One footstep can break coral that has taken over 10 to 50 years to grow only a few centimeters.
    - **Leave Marine Organisms:** Do not take any marine organisms with you, such as shells and corals. All organisms have a role to play in the ecosystem.
    - **Anchor with Care:** Do not drop anchors on live coral or seagrass habitats. Anchors can destroy decades of coral growth in seconds.
    - **Do Not Feed Fish:** Many fish feed on algae or detritus, keeping the reef clean. Feeding them can disrupt this balance.
    - **Proper Disposal of Waste:** Do not leave rubbish behind. Beach litter usually ends up in the ocean, harming marine habitats and organisms.
    - **Snorkel Safely:** Avoid snorkeling alone if possible. It is safer to snorkel with a buddy. Inform someone (such as boathouse staff) where you are going.
    """)

# Function to create a detailed message for the AI
def get_personalized_travel_plan(user_preferences, trip_details,similar_activities, hotels, restaurants, regions, distances, route):
    hotels_list = ', '.join([hotel['Name'] for hotel in hotels])
    restaurants_list = ', '.join([restaurant['Name'] for restaurant in restaurants])

    # Extract details from similar_activities
    similar_activities_details = ""
    if similar_activities:
        similar_activities_details = "Similar activities based on your interests include: "
        similar_activities_details += ", ".join([f"{activity['Name']} - {activity['Description']}" for activity in similar_activities])
    
   
    prompt = (
    f"Create a detailed travel itinerary in {user_preferences['language_preference']} focused on attractions, restaurants, and activities which encourage eco-tourism for a trip from "
    f"{trip_details['source']} to {trip_details['destination']}, starting on {trip_details['date']}, lasting for "
    f"{trip_details['duration']} days. This should include daily timings, "
    f"preferences for {user_preferences['accommodation_preference']} accommodations, and a {user_preferences['travel_style']} travel style. "
    f"The interests include {user_preferences['interests']}, and dietary restrictions are {user_preferences['dietary_restrictions']}. The activity level is {user_preferences['activity_level']}. "
)

    if user_preferences['travel_style'] in ['Relaxed', 'Cultural', 'Family-Friendly']:
        prompt += (
            "Given the travel style is more relaxed or focused on cultural and family-friendly activities, the plan will not include changing hotels frequently, except if the trip is extended beyond a typical duration. "
        )
    else:
        prompt += (
            "For a fast-paced travel style, the itinerary will include changing hotels at least once or twice, depending on the length of the trip, to optimize the experience. "
        )

    prompt += (
        f"Include these verified eco-friendly hotels: {', '.join([hotel['Name'] for hotel in similar_hotels])}, and these restaurants: {restaurants_list}. If a specific restaurant is unknown, suggest a local one but do not invent; accurate information is crucial. "
        f"The route must be optimized, and travel time between destinations should not exceed 1 hour and 30 minutes. "
        f"Also, provide a travel checklist relevant to the destination and duration. "
        f"The optimal route based on regions is: {route}. {similar_activities_details}"
    )


    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }, json=payload)

    response_json = response.json()
    if 'choices' in response_json and response_json['choices']:
        message_content = response_json['choices'][0]['message']['content']
        return message_content
    else:
        raise ValueError("Failed to get a valid response from the OpenAI API")

# Collecting user preferences and trip details for travel planning
user_preferences = {
    'language_preference': language_preference,
    'interests': interests,
    'dietary_restrictions': dietary_restrictions,
    'activity_level': activity_level,
    # 'specific_interests': specific_interests,
    'accommodation_preference': accommodation_preference,
    'travel_style': travel_style,
    # 'must_visit_landmarks': must_visit_landmarks
}
trip_details = {
    'source': source,
    'destination': 'Mauritius',
    'date': date,
    # 'budget': budget,
    'duration': duration
}

if st.sidebar.button('Generate Travel Plan'):
    if source and date and duration:
        # Fetch data from MongoDB
        activities = fetch_data('activities')
        hotels = fetch_data('hotels')
        restaurants = fetch_data('restaurants')
        regions = fetch_data('regions')
        distance_matrix_data = fetch_data('distance_matrix')
        distances = distance_matrix_data[0]['matrix']

        # Ensure API key and MongoDB client are set up
        mongo_uri = os.getenv('MONGO_URI')
        if api_key is None:
            st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in the secrets.")
        else:
            client = OpenAI(api_key=api_key)

        mongo_client = MongoClient(mongo_uri)
        activity_collection = mongo_client['eco-activities-mu']['activities']

        # Update or generate embeddings for activities
        for activity in activities:
            if 'embedding' not in activity:
                activity['embedding'] = get_embedding(activity['Tags'])
                activity_collection.update_one(
                    {'_id': activity['_id']},
                    {'$set': {'embedding': activity['embedding']}}
                )

        # Find similar activities and accommodations
        similar_activities = find_similar_activities(user_preferences, activities, top_n=10)
        similar_hotels = find_accommodations(user_preferences, hotels, top_n=3)

        if not similar_activities:
            st.error('No similar activities found.')
            st.stop()

        # Calculate optimal route including both activities and hotels
        route = calculate_optimal_route(similar_activities, similar_hotels, distances)

        with st.spinner('Generating Travel Plan...'):
            response = get_personalized_travel_plan(user_preferences, trip_details, similar_activities, similar_hotels, restaurants, regions, distances, route)
        st.success('Here is your personalized travel plan in ' + language_preference + ':')
        st.markdown(response)
        add_conclusion()
    else:
        st.error('Please fill in all the fields to generate the travel plan.')
