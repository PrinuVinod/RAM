import pandas as pd
import requests

# tomorrow.io API details
API_KEY = '6fLiAoGmc95xh768Fl77KidyvfrmMDkl'
BASE_URL = 'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=6fLiAoGmc95xh768Fl77KidyvfrmMDkl'

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
    
    # Ensure Population column is treated as string before replacing commas
    flood_data['Population'] = flood_data['Population'].astype(str).str.replace(',', '').astype(int)
    flood_data['Severity'] = flood_data['Elevation'].apply(get_severity_based_on_elevation)

    allocated_units = {}
    total_allocated_units = 0

    for index, row in flood_data.iterrows():
        loc = row['Location']
        elevation = row['Elevation']
        severity = row['Severity']
        population = row['Population']

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
                'severity': severity,
                'population': population
            }
            continue

        if rain_mm > severity:
            total_rainfall = sum([get_rainfall(row['Location']) for _, row in flood_data.iterrows() if get_rainfall(row['Location']) > row['Severity']])
            total_population = flood_data['Population'].sum()

            weight_rainfall = rain_mm / total_rainfall if total_rainfall > 0 else 0
            weight_population = population / total_population if total_population > 0 else 0

            weight = (weight_rainfall + weight_population) / 2

            allocated_units[loc] = {
                'allocated_units': total_units_available * weight,
                'rainfall_mm': rain_mm,
                'elevation': elevation,
                'sea_level_status': sea_level_status,
                'severity': severity,
                'population': population
            }
            total_allocated_units += allocated_units[loc]['allocated_units']
        else:
            allocated_units[loc] = {
                'allocated_units': 0,
                'rainfall_mm': rain_mm,
                'elevation': elevation,
                'sea_level_status': sea_level_status,
                'severity': severity,
                'population': population
            }

    # Write results to a file
    with open('results.txt', 'w') as f:
        for loc, data in allocated_units.items():
            f.write(f"Location: {loc}\n")
            f.write(f"Units allocated: {data['allocated_units'] if data['allocated_units'] is not None else 'No data available'}\n")
            f.write(f"Current rainfall: {data['rainfall_mm'] if data['rainfall_mm'] is not None else 'No data available'} mm\n")
            f.write(f"Elevation: {data['elevation']} meters ({data['sea_level_status']})\n")
            f.write(f"Population: {data['population']}\n")
            f.write("-" * 20 + "\n")

    # Write unallocated units to a file
    units_left = total_units_available - total_allocated_units
    with open('units_left.txt', 'w') as f:
        f.write(f"{units_left}")

if __name__ == "__main__":
    main()
