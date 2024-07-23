import pandas as pd

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
    try:
        with open('total_units.txt', 'r') as f:
            total_units_available = int(f.read().strip())
    except FileNotFoundError:
        total_units_available = 0

    flood_data = pd.read_csv('flood_data.csv')
    flood_data['Severity'] = flood_data['Elevation'].apply(get_severity_based_on_elevation)
    weather_data = pd.read_csv('weather_data(2018).csv')
    
    # Print the columns of weather_data to verify the column names
    print("Weather data columns:", weather_data.columns)
    
    allocated_units = {}
    total_allocated_units = 0

    for index, row in flood_data.iterrows():
        loc = row['Location']
        elevation = row['Elevation']
        severity = row['Severity']
        population = row['Population']  # Assume 'Population' column exists in flood_data.csv

        if elevation > 0:
            sea_level_status = "Above Sea Level"
        elif elevation < 0:
            sea_level_status = "Below Sea Level"
        else:
            sea_level_status = "Sea Level"

        if loc in weather_data['Location'].values:
            rain_mm = weather_data.loc[weather_data['Location'] == loc, 'rainfall'].values[0]

            if rain_mm > severity:
                total_rainfall = weather_data[weather_data['rainfall'] > severity]['rainfall'].sum()
                weight_rainfall = rain_mm / total_rainfall
                weight_population = population / flood_data['Population'].sum()

                allocated_units[loc] = {
                    'allocated_units': total_units_available * (weight_rainfall + weight_population) / 2,
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
        else:
            allocated_units[loc] = {
                'allocated_units': None,
                'rainfall_mm': None,
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
