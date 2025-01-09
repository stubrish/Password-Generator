import tkinter as tk
from tkinter import messagebox, filedialog
import secrets
import string
import pyperclip  # For copying to clipboard
import pyttsx3  # For text-to-speech
import threading  # For running pronunciation in a separate thread
import qrcode  # For generating QR codes
from PIL import Image  # For saving QR code as an image
import math  # For entropy calculation

# Function to generate password
def generate_password(length=None):
    # Use the provided length or default to 16
    if length is None:
        length = 16  # Default length if no input is provided

    # Define character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = string.punctuation

    # Ensure at least one character from each set
    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(special),
    ]

    # Fill the rest with random characters from all sets
    all_characters = uppercase + lowercase + digits + special
    password += [secrets.choice(all_characters) for _ in range(length - 4)]

    # Shuffle the password to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)

    # Convert list to string
    password = ''.join(password)
    password_var.set(password)

    # Calculate and display entropy
    entropy = calculate_entropy(password)
    entropy_var.set(f"Password Entropy: {entropy:.2f} bits")

# Function to calculate password entropy
def calculate_entropy(password):
    # Determine the size of the character set
    charset_size = len(set(password))
    # Calculate entropy
    entropy = len(password) * math.log2(charset_size)
    return entropy

# Function to copy password to clipboard
def copy_to_clipboard():
    password = password_var.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password generated yet.")

# Function to handle customization window close
def close_customization():
    global custom_length
    if length_entry_custom.get():
        try:
            custom_length = int(length_entry_custom.get())
            if custom_length < 12:
                messagebox.showerror("Error", "Password length must be at least 12 characters.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for password length.")
            return
    else:
        custom_length = 16  # Default length if no input is provided

    if customization_window:
        customization_window.destroy()
    generate_password(custom_length)  # Generate password with the custom length

# Function to open customization window
def open_customization():
    global customization_window, length_entry_custom

    customization_window = tk.Toplevel(root)
    customization_window.title("Customization Options")
    customization_window.geometry("300x150")
    customization_window.resizable(False, False)

    # Password Length in Customization Window (Optional)
    tk.Label(customization_window, text="Password Length (min 12, optional):", font=("Arial", 10)).pack(pady=10)
    length_entry_custom = tk.Entry(customization_window, font=("Arial", 10))
    length_entry_custom.pack(pady=5)

    # Bind Enter key to close the window and generate password
    length_entry_custom.bind("<Return>", lambda event: close_customization())

    # OK Button
    tk.Button(customization_window, text="OK", command=close_customization, font=("Arial", 10)).pack(pady=10)

# Function to pronounce password
def pronounce_password():
    password = password_var.get()
    if password:
        # Replace special characters with their spoken equivalents
        special_char_map = {
            "!": "exclamation mark",
            "@": "at symbol",
            "#": "hash",
            "$": "dollar sign",
            "%": "percent sign",
            "^": "caret",
            "&": "ampersand",
            "*": "asterisk",
            "(": "left parenthesis",
            ")": "right parenthesis",
            "-": "hyphen",
            "_": "underscore",
            "=": "equals sign",
            "+": "plus sign",
            "[": "left square bracket",
            "]": "right square bracket",
            "{": "left curly brace",
            "}": "right curly brace",
            "|": "vertical bar",
            "\\": "backslash",
            ";": "semicolon",
            ":": "colon",
            "'": "apostrophe",
            '"': "quotation mark",
            ",": "comma",
            "<": "less than sign",
            ".": "period",
            ">": "greater than sign",
            "/": "forward slash",
            "?": "question mark",
            "`": "backtick",
            "~": "tilde"
        }
        pronounceable_password = " ".join([special_char_map.get(char, char) for char in password])
        
        # Run pronunciation in a separate thread
        threading.Thread(target=speak_password, args=(pronounceable_password,), daemon=True).start()
    else:
        messagebox.showerror("Error", "No password generated yet.")

# Function to speak password (runs in a separate thread)
def speak_password(pronounceable_password):
    engine = pyttsx3.init()  # Reinitialize the engine
    engine.setProperty("rate", 150)  # Slow down the speech rate (default is 200)
    engine.say(pronounceable_password)
    engine.runAndWait()

# Function to stop pronunciation
def stop_pronunciation():
    engine = pyttsx3.init()  # Reinitialize the engine
    engine.stop()  # Stop the engine

# Function to generate and save QR code
def generate_qr_code():
    password = password_var.get()
    if password:
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(password)
        qr.make(fit=True)
        qr_img = qr.make_image(fill="black", back_color="white")

        # Prompt user to save the QR code
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            qr_img.save(file_path)
            messagebox.showinfo("Saved", "QR code saved successfully!")
    else:
        messagebox.showerror("Error", "No password generated yet.")

# Create the main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x450")  # Adjusted height
root.resizable(False, False)

# Variables
password_var = tk.StringVar()
entropy_var = tk.StringVar()
custom_length = None
customization_window = None
length_entry_custom = None

# Styling
font_style = ("Arial", 12)

# Customize Button
tk.Button(root, text="Customize", command=open_customization, font=font_style).pack(pady=10)

# Generate Button
tk.Button(root, text="Generate Password", command=lambda: generate_password(custom_length), font=font_style).pack(pady=10)

# Generated Password Display
tk.Label(root, text="Generated Password:", font=font_style).pack(pady=5)
password_entry = tk.Entry(root, textvariable=password_var, state="readonly", font=font_style, width=25)
password_entry.pack(pady=5)

# Password Entropy Display
tk.Label(root, textvariable=entropy_var, font=font_style).pack(pady=5)

# Copy Button
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=font_style).pack(pady=10)

# Pronounce and Stop Buttons (placed next to each other)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Pronounce Password Button
pronounce_button = tk.Button(button_frame, text="Pronounce Password", command=pronounce_password, font=font_style)
pronounce_button.pack(side=tk.LEFT, padx=5)

# Stop Pronunciation Button
stop_button = tk.Button(button_frame, text="Stop Pronunciation", command=stop_pronunciation, font=font_style)
stop_button.pack(side=tk.LEFT, padx=5)

# Generate QR Code Button
tk.Button(root, text="Generate QR Code", command=generate_qr_code, font=font_style).pack(pady=10)

# Run the application
root.mainloop()