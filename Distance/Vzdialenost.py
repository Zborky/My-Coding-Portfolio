import pandas as pd
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import os

# API key for OpenCage
key = ""  # Insert your actual API key here
geocoder = OpenCageGeocode(key)

def get_coordinates(city_name):
    """
    Retrieve coordinates for a given city name using OpenCage geocoding API.
    
    Args:
        city_name (str): The name of the city to geocode.
    
    Returns:
        tuple: A tuple containing latitude and longitude of the city, or None if the city is not found.
    """
    try:
        results = geocoder.geocode(city_name)
        if results and len(results) > 0:
            return (results[0]['geometry']['lat'], results[0]['geometry']['lng'])
        else:
            print(f"No coordinates found for city: {city_name}")
            return None
    except Exception as e:
        print(f"Error while geocoding city {city_name}: {e}")
        return None

def calculate_distance(coord1, coord2):
    """
    Calculate the distance between two coordinates using geodesic distance.
    
    Args:
        coord1 (tuple): Latitude and longitude of the first location.
        coord2 (tuple): Latitude and longitude of the second location.
    
    Returns:
        float: The distance in kilometers between the two coordinates, or None if any coordinate is None.
    """
    if coord1 and coord2:
        return geodesic(coord1, coord2).kilometers
    else:
        return None

# Define file paths for input and output Excel files
input_file_path = "C:/Users/Jakub/Desktop/Python/Vzdialenost/nazvy_miest.xlsx"
output_file_path = "C:/Users/Jakub/Desktop/Python/Vzdialenost/nazvy_miest_s_vzdialenostami.xlsx"

# Check if the input file exists
if not os.path.exists(input_file_path):
    print(f"Error: File {input_file_path} does not exist.")
else:
    # Load the Excel file into a DataFrame
    df = pd.read_excel(input_file_path)

    # Assume columns contain city names in 'Mesto1' and 'Mesto2'
    df['Distance (km)'] = None

    # Iterate through each row and calculate the distance
    for index, row in df.iterrows():
        city1 = row['Mesto1']
        city2 = row['Mesto2']
        print(f"Processing pair: {city1} - {city2}")
        coord1 = get_coordinates(city1)
        coord2 = get_coordinates(city2)
        if coord1 and coord2:
            distance = calculate_distance(coord1, coord2)
            df.at[index, 'Distance (km)'] = distance
            print(f"Coordinates: {city1} -> {coord1}, {city2} -> {coord2}")
            print(f"Distance: {distance:.2f} km\n")
        else:
            print(f"Unable to get coordinates for cities {city1} and {city2}.")

    # Save the results back to an Excel file
    df.to_excel(output_file_path, index=False)

    print(f"Calculations completed and results saved to {output_file_path}")
