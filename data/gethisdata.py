import pandas as pd

# Example function to fetch flood data for a specific location and event
def fetch_flood_data(location, event):
    # Replace with actual data fetching logic from reliable sources
    # Example placeholders:
    if location == "Alappuzha" and event == "2018 Kerala Floods":
        return {
            'Date': 'August 2018',  # Replace with actual date
            'Location': 'Alappuzha',
            'Severity': 'High',  # Replace with severity level
            'Rain Frequency (mm)': 300  # Replace with actual rain frequency data
        }
    elif location == "Alappuzha" and event == "2019 Floods":
        return {
            'Date': 'September 2019',  # Replace with actual date
            'Location': 'Alappuzha',
            'Severity': 'Moderate',  # Replace with severity level
            'Rain Frequency (mm)': 150  # Replace with actual rain frequency data
        }
    elif location == "Alappuzha" and event == "2020 Floods":
        return {
            'Date': 'October 2020',  # Replace with actual date
            'Location': 'Alappuzha',
            'Severity': 'Extreme',  # Replace with severity level
            'Rain Frequency (mm)': 500  # Replace with actual rain frequency data
        }
    # Add more conditions for other locations and events as needed

    # If data is not found for a specific location and event
    print(f"Data not found for {location} during {event}.")
    return None

# Example locations and events
locations = ["Alappuzha", "Ambalappuzha", "Haripad", "Chengannur", "Mavelikkara", 
             "Kayamkulam", "Kuttanad", "Cherthala", "Arror"]
events = ["2018 Kerala Floods", "2019 Floods", "2020 Floods"]  # Example flood events

# Initialize empty list to store data
data = []

# Iterate over locations and events to fetch data
for location in locations:
    for event in events:
        flood_data = fetch_flood_data(location, event)
        if flood_data:
            data.append(flood_data)

# Convert data to pandas DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV file
csv_filename = 'historical_data.csv'
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
