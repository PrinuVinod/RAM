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
    flood_data = pd.read_csv('flood_data.csv')
    flood_data['Severity'] = flood_data['Elevation'].apply(get_severity_based_on_elevation)
    weather_data = pd.read_csv('weather_data(2012).csv')
    total_units_available = int(input("Enter the number of units available (1 unit = resources for 1 person): "))
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
        
        if loc in weather_data['Location'].values:
            rain_mm = weather_data.loc[weather_data['Location'] == loc, 'rainfall'].values[0]
            
            if rain_mm > severity:
                total_rainfall = weather_data[weather_data['rainfall'] > severity]['rainfall'].sum()
                weight = rain_mm / total_rainfall
                
                allocated_units[loc] = {
                    'allocated_units': total_units_available * weight,
                    'rainfall_mm': rain_mm,
                    'elevation': elevation,
                    'sea_level_status': sea_level_status,
                    'severity': severity
                }
            else:
                print(f"Location: {loc}")
                print(f"Current rainfall: {rain_mm} mm is below the severity threshold of {severity} mm.")
                print("No units allocated.")
                print("-" * 20)
        else:
            print(f"Warning: No rainfall data found for {loc}. Skipping this location.")
    
    for loc, data in allocated_units.items():
        print(f"Location: {loc}")
        print(f"Units allocated: {data['allocated_units']:.2f}")
        print(f"Current rainfall: {data['rainfall_mm']} mm")
        print(f"Elevation: {data['elevation']} meters {data['sea_level_status']}")
        print(f"Severity (rainfall needed to cause flood): {data['severity']} mm")
        print("-" * 20)

if __name__ == "__main__":
    main()
