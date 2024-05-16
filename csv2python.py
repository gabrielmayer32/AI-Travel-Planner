import csv

# Function to convert CSV to list of dictionaries
def csv_to_list_of_dicts(csv_file_path):
    activities = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                region_id = int(row["Region ID"]) if row["Region ID"].strip() else 0  # Default to 0 if empty
                activity = {
                    "ID": int(row["ID"]),
                    "Name": row["Name"],
                    "Tags": row["Tags"],
                    "Dietary": row["Dietary"],
                    "Location": row["Location"],
                    "GPS": row["GPS"],
                    "Description": row["Description"],
                    "Duration": row["Duration"],
                    "Region ID": region_id
                }
                activities.append(activity)
            except ValueError as e:
                print(f"Error processing row: {row} - {e}")
                continue  # Skip rows with invalid data
    return activities

csv_file_path = 'database_schema - database_schema.csv'

# Convert CSV to list of dictionaries
activities = csv_to_list_of_dicts(csv_file_path)

# Print the result
print(activities)
