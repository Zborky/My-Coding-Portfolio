import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import ttkbootstrap as ttkb

def get_weather(city):
    """
    Fetches current weather for the given city from the OpenWeatherMap API.

    Parameters:
    city (str): The name of the city for which to get the weather.

    Returns:
    tuple: Contains weather icon URL, temperature (in °C), weather description, city name, and country.
           Returns None if the city is not found.
    """
    API_key = "0a30dd8a5e2d97d75744dda4dc15e4e7"  # API key for OpenWeatherMap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    
    # Send GET request to OpenWeatherMap API
    res = requests.get(url)
    
    # Check if the city was found
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    # Process the JSON response
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    description = weather['weather'][0]['description']
    country = weather['sys']['country']

    # Create URL for the weather icon
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"  
    return (icon_url, temperature, description, city, country)  

def search():
    """
    Retrieves weather data for the user-entered city and updates the GUI.
    """
    city = city_entry.get()  # Get the city name from the input field
    result = get_weather(city)  # Get weather data
    if result is None:
        return  # Exit the function if city is not found

    icon_url, temperature, description, city, country = result

    # Update the text for the city and country
    location_label.config(text=f"{city}, {country}")

    # Load and display the weather icon
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.config(image=icon)
    icon_label.image = icon  # Keep a reference to the image

    # Update text for temperature and weather description
    temperature_label.config(text=f"Temperature: {temperature:.2f}°C")
    description_label.config(text=f"Description: {description}")

# Create the main application window with a theme
root = ttkb.Window(themename="morph")
root.title("Weather App")  # Set the window title
root.geometry("400x400")   # Set the window size

# Create and place GUI elements
city_entry = ttkb.Entry(root, font=("Helvetica", 18))  # Input field for city name
city_entry.pack(pady=10)

search_button = ttkb.Button(root, text="Search", command=search, bootstyle="Warning")  # Button to perform search
search_button.pack(pady=10)

location_label = tk.Label(root, font=("Helvetica", 25))  # Label to display city and country
location_label.pack(pady=20)

icon_label = tk.Label(root)  # Label to display the weather icon
icon_label.pack()

temperature_label = tk.Label(root, font=("Helvetica", 20))  # Label to display temperature
temperature_label.pack()

description_label = tk.Label(root, font=("Helvetica", 20))  # Label to display weather description
description_label.pack()

# Start the main application loop
root.mainloop()