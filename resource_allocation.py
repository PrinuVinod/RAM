import pandas as pd
import requests

# OpenWeatherMap API details
API_KEY = 'bf2bdb4a714aed3a1a8e0d17644f9536'  # Replace with your OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_rainfall(location):
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    
    # Check if the response contains valid JSON
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Error: Unable to fetch weather data for {location}. Please check your API key and internet connection.")
        return None

    if response.status_code == 200:
        # Get rainfall in the last 1 hour if available, otherwise use 0
        rain_mm = data.get('rain', {}).get('1h', 0)
        return rain_mm
    else:
        print(f"Error fetching weather data for {location}:", data.get('message', 'Unknown error'))
        return None

def main():
    # Load locations from CSV file
    flood_data = pd.read_csv('flood_data.csv')
    
    # User input for total units available
    total_units_available = int(input("Enter the number of units available (1 unit = resources for 1 person): "))
    
    # Calculate units per location
    num_locations = len(flood_data)
    units_per_location = total_units_available / num_locations
    
    # Initialize a dictionary to store allocated units and rainfall for each location
    allocated_units = {}

    # Iterate through each location in the dataset
    for loc in flood_data['Location']:
        # Get live rainfall data for the current location
        rain_mm = get_rainfall(loc)
        
        if rain_mm is None:
            continue
        
        # Calculate units allocated for the current location based on units per location
        allocated_units[loc] = {
            'allocated_units': rain_mm * units_per_location,
            'rainfall_mm': rain_mm
        }
    
    # Print the allocated units and rainfall for each location
    for loc, data in allocated_units.items():
        print(f"Location: {loc}")
        print(f"Units allocated: {data['allocated_units']:.2f}")
        print(f"Current rainfall: {data['rainfall_mm']} mm")
        print("-" * 20)

if __name__ == "__main__":
    main()
