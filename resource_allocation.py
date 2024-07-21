import pandas as pd

def main():
    # Load locations and rainfall data from CSV files
    flood_data = pd.read_csv('flood_data.csv')
    weather_data = pd.read_csv('weather_data(2012).csv')
    
    # User input for total units available
    total_units_available = int(input("Enter the number of units available (1 unit = resources for 1 person): "))
    
    # Calculate the total rainfall across all locations
    total_rainfall = weather_data['rainfall'].sum()
    
    # Initialize a dictionary to store allocated units, elevation, and sea level status for each location
    allocated_units = {}

    # Iterate through each location in the dataset
    for index, row in flood_data.iterrows():
        loc = row['Location']
        elevation = row['Elevation']
        
        # Determine sea level status
        if elevation > 0:
            sea_level_status = "Above Sea Level"
        elif elevation < 0:
            sea_level_status = "Below Sea Level"
        else:
            sea_level_status = "Sea Level"
        
        # Check if the location exists in the weather_data.csv file
        if loc in weather_data['Location'].values:
            # Get rainfall data for the current location from the weather_data.csv file
            rain_mm = weather_data.loc[weather_data['Location'] == loc, 'rainfall'].values[0]
            
            # Calculate the relative weight of the current location's rainfall
            weight = rain_mm / total_rainfall
            
            # Calculate units allocated for the current location based on the relative weight
            allocated_units[loc] = {
                'allocated_units': total_units_available * weight,
                'rainfall_mm': rain_mm,
                'elevation': elevation,
                'sea_level_status': sea_level_status
            }
        else:
            print(f"Warning: No rainfall data found for {loc}. Skipping this location.")
    
    # Print the allocated units, elevation, and sea level status for each location
    for loc, data in allocated_units.items():
        print(f"Location: {loc}")
        print(f"Units allocated: {data['allocated_units']:.2f}")
        print(f"Current rainfall: {data['rainfall_mm']} mm")
        print(f"Elevation: {data['elevation']} meters {data['sea_level_status']}")
        print("-" * 20)

if __name__ == "__main__":
    main()
