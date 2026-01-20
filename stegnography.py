import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import pyttsx3
import os

# ------------------ GLOBAL VARIABLES ------------------
image_path = ""
stego_image_path = "stego_image.png"
extracted_char = ""
preview_photo = None

# ------------------ TEXT TO SPEECH ------------------
def speak_char():
    global extracted_char
    if extracted_char == "":
        return
    engine = pyttsx3.init()
    engine.say(extracted_char)
    engine.runAndWait()

# ------------------ STEGANOGRAPHY ------------------
def hide_character():
    global image_path

    if image_path == "":
        messagebox.showerror("Error", "Please select an image first")
        return

    char = char_entry.get()
    if len(char) != 1:
        messagebox.showerror("Error", "Enter exactly ONE character")
        return

    img = Image.open(image_path).convert("L")
    img = img.resize((128, 128))
    data = np.array(img, dtype=np.uint8)

    binary = format(ord(char), '08b')
    flat = data.flatten()

    for i in range(8):
        flat[i] = (flat[i] & 254) | int(binary[i])

    stego_img = flat.reshape(data.shape)
    Image.fromarray(stego_img).save(stego_image_path)

    messagebox.showinfo("Success", "Character hidden successfully!")

def extract_character():
    global extracted_char

    if not os.path.exists(stego_image_path):
        messagebox.showerror("Error", "Stego image not found")
        return

    img = Image.open(stego_image_path).convert("L")
    data = np.array(img, dtype=np.uint8).flatten()

    binary = ''.join(str(data[i] & 1) for i in range(8))
    extracted_char = chr(int(binary, 2))

    result_label.config(text=f"Hidden Character: {extracted_char}")

    speak_char()  # 🔊 AUTO PLAY

# ------------------ IMAGE SELECTION + PREVIEW ------------------
def select_image():
    global image_path, preview_photo

    image_path = filedialog.askopenfilename(
        filetypes=[("JPEG Images", "*.jpg *.jpeg")]
    )

    if image_path:
        img = Image.open(image_path).convert("L")
        img = img.resize((128, 128))

        preview_photo = ImageTk.PhotoImage(img)
        image_preview_label.config(image=preview_photo)

        image_label.config(
            text="Selected Image (Grayscale 128 × 128)",
            fg="#2c3e50"
        )

# ------------------ UI ------------------
root = tk.Tk()
root.title("Image Steganography with AI Speech")
root.geometry("460x600")
root.configure(bg="#f4f6f7")

# ------------------ HEADING ------------------
tk.Label(
    root,
    text="Image Steganography System",
    font=("Helvetica", 18, "bold"),
    bg="#f4f6f7",
    fg="#1a5276"
).pack(pady=15)

tk.Label(
    root,
    text="Hide a Character in an Image and Retrieve it with AI Speech",
    font=("Helvetica", 10),
    bg="#f4f6f7",
    fg="#566573"
).pack(pady=5)

# ------------------ SELECT IMAGE ------------------
tk.Button(
    root,
    text="Select Image",
    command=select_image,
    width=25,
    bg="#3498db",
    fg="white",
    font=("Helvetica", 10, "bold")
).pack(pady=10)

image_label = tk.Label(
    root,
    text="No image selected",
    bg="#f4f6f7",
    fg="#7f8c8d"
)
image_label.pack()

image_preview_label = tk.Label(root, bg="#f4f6f7")
image_preview_label.pack(pady=12)

# ------------------ CHARACTER INPUT ------------------
tk.Label(
    root,
    text="Enter ONE Character to Hide",
    bg="#f4f6f7",
    font=("Helvetica", 11)
).pack(pady=5)

char_entry = tk.Entry(root, width=10, font=("Helvetica", 12), justify="center")
char_entry.pack(pady=5)

# ------------------ ACTION BUTTONS ------------------
tk.Button(
    root,
    text="Hide Character",
    command=hide_character,
    width=25,
    bg="#27ae60",
    fg="white",
    font=("Helvetica", 10, "bold")
).pack(pady=10)

tk.Button(
    root,
    text="Extract Character (Auto Speak)",
    command=extract_character,
    width=25,
    bg="#e67e22",
    fg="white",
    font=("Helvetica", 10, "bold")
).pack(pady=10)

# ------------------ RESULT ------------------
result_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 13, "bold"),
    bg="#f4f6f7",
    fg="#1a5276"
)
result_label.pack(pady=15)

root.mainloop()
