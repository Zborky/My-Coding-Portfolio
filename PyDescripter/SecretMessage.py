import tkinter as tk
from tkinter import messagebox

def vigenere_encrypt(plaintext, key):
    """
    Šifruje zadaný text pomocou Vigenèrovej šifry.

    Args:
        plaintext (str): Text, ktorý sa má zašifrovať.
        key (str): Kľúč na šifrovanie.

    Returns:
        str: Zašifrovaný text.
    """
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Odstránenie medzier a zmena textu a kľúča na veľké písmená
    plaintext = plaintext.replace(' ', '').upper()
    key = key.replace(' ', '').upper()
    key_length = len(key)
    ciphertext = []
    key_index = 0
    
    # Šifrovanie každého znaku v plaintext
    for char in plaintext:
        if char in alphabet:
            shift = alphabet.index(key[key_index % key_length])
            new_index = (alphabet.index(char) + shift) % len(alphabet)
            ciphertext.append(alphabet[new_index])
            key_index += 1
        else:
            # Pridanie znaku bez zmeny, ak nie je v abecede
            ciphertext.append(char)
    
    return ''.join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    """
    Dešifruje zadaný text pomocou Vigenèrovej šifry.

    Args:
        ciphertext (str): Text, ktorý sa má dešifrovať.
        key (str): Kľúč na dešifrovanie.

    Returns:
        str: Dešifrovaný text.
    """
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Odstránenie medzier a zmena textu a kľúča na veľké písmená
    ciphertext = ciphertext.replace(' ', '').upper()
    key = key.replace(' ', '').upper()
    key_length = len(key)
    plaintext = []
    key_index = 0
    
    # Dešifrovanie každého znaku v ciphertext
    for char in ciphertext:
        if char in alphabet:
            shift = alphabet.index(key[key_index % key_length])
            new_index = (alphabet.index(char) - shift) % len(alphabet)
            plaintext.append(alphabet[new_index])
            key_index += 1
        else:
            # Pridanie znaku bez zmeny, ak nie je v abecede
            plaintext.append(char)
    
    return ''.join(plaintext)

def encrypt_text():
    """
    Funkcia na šifrovanie textu na základe vstupov v GUI.
    """
    plaintext = plaintext_entry.get()
    key = key_entry.get()
    if not key:
        messagebox.showerror("Error", "Key cannot be empty")
        return
    encrypted_text = vigenere_encrypt(plaintext, key)
    result_text.set(f"Encrypted: {encrypted_text}")

def decrypt_text():
    """
    Funkcia na dešifrovanie textu na základe vstupov v GUI.
    """
    ciphertext = plaintext_entry.get()
    key = key_entry.get()
    if not key:
        messagebox.showerror("Error", "Key cannot be empty")
        return
    decrypted_text = vigenere_decrypt(ciphertext, key)
    result_text.set(f"Decrypted: {decrypted_text}")

# Vytvorenie hlavného okna aplikácie
root = tk.Tk()
root.title("Vigenère Cipher")

# Vytvorenie textového poľa na zadanie textu
tk.Label(root, text="Text:").pack(pady=5)
plaintext_entry = tk.Entry(root, width=50)
plaintext_entry.pack(pady=5)

# Vytvorenie textového poľa na zadanie kľúča
tk.Label(root, text="Key:").pack(pady=5)
key_entry = tk.Entry(root, width=50)
key_entry.pack(pady=5)

# Tlačidlo na šifrovanie textu
tk.Button(root, text="Encrypt", command=encrypt_text).pack(pady=5)

# Tlačidlo na dešifrovanie textu
tk.Button(root, text="Decrypt", command=decrypt_text).pack(pady=5)

# Pole na zobrazenie výsledku
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text).pack(pady=10)

# Spustenie hlavnej slučky GUI
root.mainloop()