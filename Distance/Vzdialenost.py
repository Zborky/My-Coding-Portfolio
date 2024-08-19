import pandas as pd
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import os

# API kľúč pre OpenCage
key = "7d8a69b6a38342cc87ce6a629eb65989"  # Sem vlož svoj skutočný API kľúč
geocoder = OpenCageGeocode(key)

def get_coordinates(city_name):
    try:
        results = geocoder.geocode(city_name)
        if results and len(results) > 0:
            return (results[0]['geometry']['lat'], results[0]['geometry']['lng'])
        else:
            print(f"Nenájdené súradnice pre mesto: {city_name}")
            return None
    except Exception as e:
        print(f"Chyba pri geokódovaní mesta {city_name}: {e}")
        return None

def calculate_distance(coord1, coord2):
    if coord1 and coord2:
        return geodesic(coord1, coord2).kilometers
    else:
        return None

# Definovanie ciest k Excel súborom
input_file_path = "C:/Users/Jakub/Desktop/Python/Vzdialenost/nazvy_miest.xlsx"
output_file_path = "C:/Users/Jakub/Desktop/Python/Vzdialenost/nazvy_miest_s_vzdialenostami.xlsx"

# Kontrola existencie vstupného súboru
if not os.path.exists(input_file_path):
    print(f"Chyba: Súbor {input_file_path} neexistuje.")
else:
    # Načítanie Excel súboru
    df = pd.read_excel(input_file_path)

    # Predpokladám, že stĺpce obsahujú názvy miest v stĺpcoch 'Mesto1' a 'Mesto2'
    df['Vzdialenost (km)'] = None

    # Iterovanie cez každý riadok a výpočet vzdialenosti
    for index, row in df.iterrows():
        city1 = row['Mesto1']
        city2 = row['Mesto2']
        print(f"Spracovanie dvojice: {city1} - {city2}")
        coord1 = get_coordinates(city1)
        coord2 = get_coordinates(city2)
        if coord1 and coord2:
            distance = calculate_distance(coord1, coord2)
            df.at[index, 'Vzdialenost (km)'] = distance
            print(f"Súradnice: {city1} -> {coord1}, {city2} -> {coord2}")
            print(f"Vzdialenosť: {distance:.2f} km\n")
        else:
            print(f"Nie je možné získať súradnice pre mestá {city1} a {city2}.")

    # Uloženie výsledkov späť do Excel súboru
    df.to_excel(output_file_path, index=False)

    print(f"Výpočty dokončené a výsledky uložené do {output_file_path}")