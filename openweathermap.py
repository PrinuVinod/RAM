import pandas as pd
import requests

# OpenWeatherMap API details
API_KEY = 'bf2bdb4a714aed3a1a8e0d17644f9536'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_rainfall(location):
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Error: Unable to fetch weather data for {location}.")
        return None

    if response.status_code == 200:
        rain_mm = data.get('rain', {}).get('1h', 0)
        return rain_mm
    else:
        print(f"Error fetching weather data for {location}: {data.get('message', 'Unknown error')}")
        return None

def get_severity_based_on_elevation(elevation):
    if elevation <= 1:
        return 50
    elif elevation <= 5:
        return 100
    elif elevation <= 10:
        return 150
    else:
        return 200

def main():
    # Read number of units from file
    try:
        with open('total_units.txt', 'r') as f:
            total_units_available = int(f.read().strip())
    except FileNotFoundError:
        total_units_available = 0

    flood_data = pd.read_csv('flood_data.csv')
    flood_data['Severity'] = flood_data['Elevation'].apply(get_severity_based_on_elevation)

    allocated_units = {}

    for index, row in flood_data.iterrows():
        loc = row['Location']
        elevation = row['Elevation']
        severity = row['Severity']

        if elevation > 0:
            sea_level_status = "Above Sea Level"
        elif elevation < 0:
            sea_level_status = "Below Sea Level"
        else:
            sea_level_status = "Sea Level"

        # Get live rainfall data
        rain_mm = get_rainfall(loc)
        
        if rain_mm is None:
            allocated_units[loc] = {
                'allocated_units': None,
                'rainfall_mm': None,
                'elevation': elevation,
                'sea_level_status': sea_level_status,
                'severity': severity
            }
            continue

        # Only allocate units if rainfall exceeds the severity for the given location
        if rain_mm > severity:
            # Calculate the relative weight of the current location's rainfall
            total_rainfall = sum([get_rainfall(row['Location']) for _, row in flood_data.iterrows() if get_rainfall(row['Location']) > row['Severity']])
            weight = rain_mm / total_rainfall if total_rainfall > 0 else 0

            allocated_units[loc] = {
                'allocated_units': total_units_available * weight,
                'rainfall_mm': rain_mm,
                'elevation': elevation,
                'sea_level_status': sea_level_status,
                'severity': severity
            }
        else:
            allocated_units[loc] = {
                'allocated_units': 0,
                'rainfall_mm': rain_mm,
                'elevation': elevation,
                'sea_level_status': sea_level_status,
                'severity': severity
            }

    # Write results to a file
    with open('results.txt', 'w') as f:
        for loc, data in allocated_units.items():
            f.write(f"Location: {loc}\n")
            f.write(f"Units allocated: {data['allocated_units'] if data['allocated_units'] is not None else 'No data available'}\n")
            f.write(f"Current rainfall: {data['rainfall_mm'] if data['rainfall_mm'] is not None else 'No data available'} mm\n")
            f.write(f"Elevation: {data['elevation']} meters ({data['sea_level_status']})\n")
            f.write(f"Severity: {data['severity']} mm\n")
            f.write("-" * 20 + "\n")

if __name__ == "__main__":
    main()