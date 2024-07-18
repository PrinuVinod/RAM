import pandas as pd
import requests

# Load data
flood_data = pd.read_csv('flood_data.csv')

# OpenWeatherMap API details
API_KEY = 'bf2bdb4a714aed3a1a8e0d17644f9536'  # Replace with your OpenWeatherMap API key
BASE_URL = 'api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=bf2bdb4a714aed3a1a8e0d17644f9536'

# Define resource allocation logic
def allocate_resources(rain_mm, location):
    # Filter flood data for the location
    location_data = flood_data[flood_data['Location'] == location]
    
    # Determine the severity based on rain_mm (simple example, customize as needed)
    if rain_mm > 200:
        severity = 'Severe'
    elif rain_mm > 100:
        severity = 'Moderate'
    else:
        severity = 'Mild'
    
    # Calculate average impact for the severity
    avg_impact = location_data[location_data['Severity'] == severity]['Impact'].mean()
    
    # Define total units needed
    total_units = avg_impact  # This can be adjusted based on specific needs
    
    return total_units

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
        print("Error: Unable to fetch weather data. Please check your API key and internet connection.")
        return None

    if response.status_code == 200:
        # Get rainfall in the last 1 hour if available, otherwise use 0
        rain_mm = data.get('rain', {}).get('1h', 0)
        return rain_mm
    else:
        print("Error fetching weather data:", data.get('message', 'Unknown error'))
        return None

def main():
    # User input for location
    location = input("Enter the location (Alappuzha, Ambalappuzha, Haripad, Chengannur, Mavelikkara, Kayamkulam, Kuttanad, Cherthala, Arror): ")
    
    if location not in flood_data['Location'].unique():
        print("Invalid location. Please enter one of the specified locations.")
        return
    
    # Get live rainfall data
    rain_mm = get_rainfall(location)
    
    if rain_mm is None:
        return
    
    # Allocate resources
    total_units = allocate_resources(rain_mm, location)
    
    # Print the results
    print(f"Total units allocated for {location} with {rain_mm} mm rain: {total_units}")

if __name__ == "__main__":
    main()
