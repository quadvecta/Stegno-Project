import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
import cv2
import os
import base64
from cryptography.fernet import Fernet
import numpy as np

class StegoApp:
    def __init__(self, master):
        self.master = master
        master.title("Steganography Suite v2.1")
        self.create_help_menu()
        self.create_encrypt_ui()
        self.create_decrypt_ui()

    def create_help_menu(self):
        menubar = Menu(self.master)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.master.config(menu=menubar)

    def show_help(self):
        help_text = """
        Steganography Suite v2.1
        ------------------------
        1. Select an image for encryption/decryption.
        2. Enter your secret message or decryption key.
        3. Click 'Encrypt' or 'Decrypt' to process.
        """
        messagebox.showinfo("Help", help_text)

    def create_encrypt_ui(self):
        frame = ttk.Frame(self.master)
        frame.pack(padx=10, pady=10)

        # Image Selection
        ttk.Label(frame, text="Source Image:").grid(row=0, column=0, padx=5, pady=5)
        self.src_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.src_path, width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.src_path.set(filedialog.askopenfilename())).grid(row=0, column=2, padx=5, pady=5)

        # Secret Message
        ttk.Label(frame, text="Secret Message:").grid(row=1, column=0, padx=5, pady=5)
        self.secret_msg = tk.Text(frame, height=5, width=40)
        self.secret_msg.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Encryption Button
        ttk.Button(frame, text="Encrypt Message", command=self.encrypt).grid(row=2, column=1, pady=10)

        # Key Display
        ttk.Label(frame, text="Decryption Key:").grid(row=3, column=0, padx=5, pady=5)
        self.key_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.key_var, state="readonly", width=40).grid(row=3, column=1, padx=5, pady=5)

    def create_decrypt_ui(self):
        frame = ttk.Frame(self.master)
        frame.pack(padx=10, pady=10)

        # Encrypted Image Selection
        ttk.Label(frame, text="Encrypted Image:").grid(row=0, column=0, padx=5, pady=5)
        self.encrypted_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.encrypted_path, width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=lambda: self.encrypted_path.set(filedialog.askopenfilename())).grid(row=0, column=2, padx=5, pady=5)

        # Decryption Key
        ttk.Label(frame, text="Decryption Key:").grid(row=1, column=0, padx=5, pady=5)
        self.decrypt_key = tk.StringVar()
        ttk.Entry(frame, textvariable=self.decrypt_key, width=40).grid(row=1, column=1, padx=5, pady=5)

        # Decryption Button
        ttk.Button(frame, text="Decrypt Message", command=self.decrypt).grid(row=2, column=1, pady=10)

        # Result Display
        ttk.Label(frame, text="Decrypted Message:").grid(row=3, column=0, padx=5, pady=5)
        self.result_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.result_var, state="readonly", width=40).grid(row=3, column=1, padx=5, pady=5)

    def encrypt(self):
        img_path = self.src_path.get()
        msg = self.secret_msg.get("1.0", tk.END).strip()

        if not img_path:
            messagebox.showerror("Error", "Please select an image file.")
            return
        if not msg:
            messagebox.showerror("Error", "Please enter a secret message.")
            return

        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Unsupported image format or corrupted file.")

            key = Fernet.generate_key()
            cipher = Fernet(key)

            # Encrypt and encode message
            encrypted = cipher.encrypt(msg.encode())
            encoded = base64.b64encode(encrypted).decode()

            # Add length header
            length = len(encoded).to_bytes(4, 'big')
            full_msg = ''.join([chr(b) for b in length]) + encoded

            # Check capacity
            if len(full_msg) > img.shape[0] * img.shape[1]:
                messagebox.showerror("Error", "Message too large for selected image.")
                return

            # Embed message
            n, m, z = 0, 0, 0
            for char in full_msg:
                img[n, m, z] = ord(char)
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3

            # Save as PNG
            cv2.imwrite("secret_image.png", img)
            self.key_var.set(key.decode())
            messagebox.showinfo("Success", "Message encrypted and saved as secret_image.png")

        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def decrypt(self):
        img_path = self.encrypted_path.get()
        key = self.decrypt_key.get()

        if not img_path:
            messagebox.showerror("Error", "Please select an encrypted image.")
            return
        if not key:
            messagebox.showerror("Error", "Please enter the decryption key.")
            return

        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Unsupported image format or corrupted file.")

            # Extract length header
            n, m, z = 0, 0, 0
            length_chars = []
            for _ in range(4):
                length_chars.append(chr(img[n, m, z]))
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3

            length = int.from_bytes(bytes([ord(c) for c in length_chars]), 'big')

            # Extract message
            extracted = []
            for _ in range(length):
                extracted.append(chr(img[n, m, z]))
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3

            cipher = Fernet(key.encode())
            decrypted = cipher.decrypt(base64.b64decode(''.join(extracted))).decode()
            self.result_var.set(decrypted)

        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
