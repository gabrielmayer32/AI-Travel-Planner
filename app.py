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
accommodation_preference = st.sidebar.selectbox('Accommodation Preference', ['Hotel', 'Lodge', 'Airbnb', 'Low budget'])
travel_style = st.sidebar.selectbox('Travel Style', ['Relaxed', 'Fast-Paced', 'Adventurous', 'Cultural', 'Family-Friendly'])
# must_visit_landmarks = st.sidebar.text_input('Must-Visit Landmarks', 'e.g., Eiffel Tower, Grand Canyon')

# Connect to MongoDB and fetch data
def fetch_data(collection_name):
    
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
def calculate_optimal_route(activities, distances):
    activity_regions = []
    for activity in activities:
        try:
            region_id = int(activity['Region ID'])
            activity_regions.append(region_id)
        except (ValueError, TypeError):
            continue  # Skip activities with invalid or missing Region ID

    if not activity_regions:
        raise ValueError("No valid Region ID found in activities")

    route = []
    visited = set()

    current_region = activity_regions[0]
    route.append(current_region)
    visited.add(current_region)

    while len(visited) < len(activity_regions):
        next_region = None
        min_distance = float('inf')
        
        for region in activity_regions:
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

# Function to create a detailed message for the AI
def get_personalized_travel_plan(user_preferences, trip_details,similar_activities, hotels, restaurants, regions, distances, route):
    hotels_list = ', '.join([hotel['Name'] for hotel in hotels])
    restaurants_list = ', '.join([restaurant['Name'] for restaurant in restaurants])

    # Extract details from similar_activities
    similar_activities_details = ""
    if similar_activities:
        similar_activities_details = "Similar activities based on your interests include: "
        similar_activities_details += ", ".join([f"{activity['Name']} - {activity['Description']}" for activity in similar_activities])
    
    # prompt = (
    #     f"Create a detailed travel itinerary in {user_preferences['language_preference']} focused on attractions, restaurants, and activities which encourage eco-tourism for a trip from "
    #     f"{trip_details['source']} to {trip_details['destination']}, starting on {trip_details['date']}, lasting for "
    #     f"{trip_details['duration']} days, within a budget of {selected_currency} {trip_details['budget']}. This should include daily timings, "
    #     f"preferences for {user_preferences['accommodation_preference']} accommodations, a {user_preferences['travel_style']} travel style, "
    #     f"and interests in {user_preferences['interests']}. Dietary restrictions include "
    #     f"{user_preferences['dietary_restrictions']}, and the activity level is {user_preferences['activity_level']}. "
    #     f"Include these verified eco-friendly hotels: {hotels_list}, and restaurants: {restaurants_list}. If you don't know what restaurant to put, suggest a local one. "
    #     f"The route must be optimized and travel time between destinations should not exceed 1 hour and 30 minutes. "
    #     f"Must-visit landmarks include {user_preferences['must_visit_landmarks']}. Also, provide a travel checklist relevant to the destination and duration. "
    #     f"The optimal route based on regions is: {route}. {similar_activities_details}"
    # )

    prompt = (
    f"Create a detailed travel itinerary in {user_preferences['language_preference']} focused on attractions, restaurants, and activities which encourage eco-tourism for a trip from "
    f"{trip_details['source']} to {trip_details['destination']}, starting on {trip_details['date']}, lasting for "
    f"{trip_details['duration']} days. This should include daily timings, "
    f"preferences for {user_preferences['accommodation_preference']} accommodations, a {user_preferences['travel_style']} travel style, "
    f"and interests in {user_preferences['interests']}. Dietary restrictions include "
    f"{user_preferences['dietary_restrictions']}, and the activity level is {user_preferences['activity_level']}. "
    f"Include these verified eco-friendly hotels: {hotels_list}, and restaurants: {restaurants_list}. If you don't know what restaurant to put, suggest a local one. "
    f"The route must be optimized and travel time between destinations should not exceed 1 hour and 30 minutes. "
    f" Also, provide a travel checklist relevant to the destination and duration. "
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
    # if source and date and budget and duration:
    if source and date and duration:
        # Fetch data from MongoDB
        activities = fetch_data('activities')
        hotels = fetch_data('hotels')
        restaurants = fetch_data('restaurants')
        regions = fetch_data('regions')
        distance_matrix_data = fetch_data('distance_matrix')
        distances = distance_matrix_data[0]['matrix']  # Ensure correct access to distance matrix

        # Generate and store embeddings for activities if they don't already have them
        mongo_uri = st.secrets('MONGO_URI')
        if mongo_uri is None:
            st.error("mongo_uri API key not found. Please set the OPENAI_API_KEY in the secrets.")
        else:
            ongo_uri = os.getenv('MONGO_URI')

        mongo_client = MongoClient(mongo_uri)
        activity_collection = mongo_client['eco-activities-mu']['activities']

        for activity in activities:
            if 'embedding' not in activity:
                activity['embedding'] = get_embedding(activity['Tags'])
                activity_collection.update_one(
                    {'_id': activity['_id']},
                    {'$set': {'embedding': activity['embedding']}}
                )

        # Example usage
        similar_activities = find_similar_activities(user_preferences, activities, top_n=10)

        if not similar_activities:
            st.error('No similar activities found.')
            st.stop()

        # # Display similar activities
        # for i, activity in enumerate(similar_activities, start=1):
        #     st.write(f"Activity {i}: {activity['Name']} - {activity['Description']}")

        # Calculate optimal route
        route = calculate_optimal_route(similar_activities, distances)

        with st.spinner('Generating Travel Plan...'):
            # response = get_personalized_travel_plan(user_preferences, trip_details, selected_currency, similar_activities, hotels, restaurants, regions, distances, route)
            response = get_personalized_travel_plan(user_preferences, trip_details, similar_activities, hotels, restaurants, regions, distances, route)
        st.success('Here is your personalized travel plan in ' + language_preference + ':')
        st.markdown(response)
    else:
        st.error('Please fill in all the fields to generate the travel plan.')


