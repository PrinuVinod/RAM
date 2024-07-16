from geopy.geocoders import Nominatim
import pandas as pd

# Locations in Alappuzha district to fetch coordinates
locations = [
    "Alappuzha",
    "Ambalappuzha",
    "Haripad",
    "Chengannur",
    "Mavelikkara",
    "Kayamkulam",
    "Kuttanad",
    "Cherthala",
    "Arror"
]

def get_coordinates(location):
    geolocator = Nominatim(user_agent="RAM-Geocoder")
    try:
        location = geolocator.geocode(location + ", Alappuzha, Kerala, India")
        return (location.latitude, location.longitude) if location else None
    except Exception as e:
        print(f"Error fetching coordinates for {location}: {e}")
        return None

def main():
    data = []
    for location in locations:
        coordinates = get_coordinates(location)
        if coordinates:
            data.append({
                "Location": location,
                "Latitude": coordinates[0],
                "Longitude": coordinates[1]
            })
    
    df = pd.DataFrame(data)
    print("Geographical coordinates fetched:")
    print(df)

    # Optional: Save to CSV
    df.to_csv("data/geographical_data.csv", index=False)
    print("Coordinates saved to 'geographical_data.csv'")

if __name__ == "__main__":
    main()
