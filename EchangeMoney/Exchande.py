import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = ''
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

def get_exchange_rate(base_currency, target_currency):
    url = f"{BASE_URL}{base_currency}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Chyba pri získavaní dát z API")
    
    data = response.json()
    rates = data['conversion_rates']
    if target_currency not in rates:
        raise Exception(f"Neznáma cieľová mena: {target_currency}")
    
    return rates[target_currency]

def convert_currency(amount, base_currency, target_currency):
    rate = get_exchange_rate(base_currency, target_currency)
    return amount * rate

def on_convert():
    try:
        amount = float(amount_entry.get())
        base_currency = base_currency_entry.get().upper()
        target_currency = target_currency_entry.get().upper()
        
        converted_amount = convert_currency(amount, base_currency, target_currency)
        result_label.config(text=f"{amount} {base_currency} je {converted_amount:.2f} {target_currency}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Vytvorenie hlavného okna
root = tk.Tk()
root.title("Prevodník Mien")

# Vytvorenie a umiestnenie widgetov
tk.Label(root, text="Množstvo na konverziu:").grid(row=0, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Základná mena (napr. USD):").grid(row=1, column=0, padx=10, pady=10)
base_currency_entry = tk.Entry(root)
base_currency_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Cieľová mena (napr. EUR):").grid(row=2, column=0, padx=10, pady=10)
target_currency_entry = tk.Entry(root)
target_currency_entry.grid(row=2, column=1, padx=10, pady=10)

convert_button = tk.Button(root, text="Konvertovať", command=on_convert)
convert_button.grid(row=3, columnspan=2, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=4, columnspan=2, pady=10)

# Spustenie hlavnej slučky aplikácie
root.mainloop()
