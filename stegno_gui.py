import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
import cv2
import os
from cryptography.fernet import Fernet
import platform

class StegoApp:
    def __init__(self, master):
        self.master = master
        master.title("Steganography Suite v2.1")

        self.style = ttk.Style()
        self.theme_var = tk.StringVar(value="System")

        self.apply_theme(self.detect_system_theme())

        self.create_menu()
        self.create_help_menu()
        self.create_encrypt_ui()
        self.create_decrypt_ui()

    def detect_system_theme(self):
        try:
            if platform.system() == "Windows":
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return "dark" if value == 0 else "light"
        except:
            pass
        return "light"

    def apply_theme(self, mode):
        if mode == "dark":
            self.style.theme_use('clam')
            self.master.configure(bg="#1e1e1e")
            self.style.configure(".", background="#1e1e1e", foreground="white", fieldbackground="#2b2b2b")
            self.style.configure("TEntry", fieldbackground="#2b2b2b", foreground="white")
            self.style.configure("TButton", background="#3a3a3a", foreground="white")
            self.style.configure("TLabel", background="#1e1e1e", foreground="white")
        elif mode == "light":
            self.style.theme_use('default')
            self.master.configure(bg="white")
            self.style.configure(".", background="white", foreground="black")
        elif mode == "blue":
            self.style.theme_use('clam')
            self.master.configure(bg="#0f172a")
            self.style.configure(".", background="#0f172a", foreground="#e0f2fe", fieldbackground="#1e293b")
        elif mode == "green":
            self.style.theme_use('clam')
            self.master.configure(bg="#022c22")
            self.style.configure(".", background="#022c22", foreground="#d1fae5", fieldbackground="#064e3b")

    def change_theme(self, choice):
        if choice == "System":
            mode = self.detect_system_theme()
        elif choice == "Dark":
            mode = "dark"
        elif choice == "Light":
            mode = "light"
        elif choice == "Blue":
            mode = "blue"
        elif choice == "Green":
            mode = "green"
        self.apply_theme(mode)

    def create_menu(self):
        menubar = Menu(self.master)

        theme_menu = Menu(menubar, tearoff=0)
        theme_menu.add_command(label="System", command=lambda: self.change_theme("System"))
        theme_menu.add_command(label="Light", command=lambda: self.change_theme("Light"))
        theme_menu.add_command(label="Dark", command=lambda: self.change_theme("Dark"))
        theme_menu.add_command(label="Blue", command=lambda: self.change_theme("Blue"))
        theme_menu.add_command(label="Green", command=lambda: self.change_theme("Green"))

        menubar.add_cascade(label="Themes", menu=theme_menu)
        self.master.config(menu=menubar)

    def create_help_menu(self):
        menubar = self.master.nametowidget(self.master.winfo_children()[0])
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)

    def show_help(self):
        help_text = """
Steganography Suite v2.1

1. Select image
2. Enter message or key
3. Encrypt or decrypt
"""
        messagebox.showinfo("Help", help_text)

    def browse_encrypt_file(self):
        self.master.update()
        self.master.lift()
        self.master.focus_force()
        file_path = filedialog.askopenfilename(parent=self.master)
        self.master.lift()
        if file_path:
            self.src_path.set(file_path)

    def browse_decrypt_file(self):
        self.master.update()
        self.master.lift()
        self.master.focus_force()
        file_path = filedialog.askopenfilename(parent=self.master)
        self.master.lift()
        if file_path:
            self.encrypted_path.set(file_path)

    def create_encrypt_ui(self):
        frame = ttk.Frame(self.master)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Source Image:").grid(row=0, column=0)
        self.src_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.src_path, width=40).grid(row=0, column=1)
        ttk.Button(frame, text="Browse", command=self.browse_encrypt_file).grid(row=0, column=2)

        ttk.Label(frame, text="Secret Message:").grid(row=1, column=0)
        self.secret_msg = tk.Text(frame, height=5, width=40)
        self.secret_msg.grid(row=1, column=1, columnspan=2)

        ttk.Button(frame, text="Encrypt Message", command=self.encrypt).grid(row=2, column=1)

        ttk.Label(frame, text="Decryption Key:").grid(row=3, column=0)
        self.key_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.key_var, state="readonly", width=40).grid(row=3, column=1)

    def create_decrypt_ui(self):
        frame = ttk.Frame(self.master)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Encrypted Image:").grid(row=0, column=0)
        self.encrypted_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.encrypted_path, width=40).grid(row=0, column=1)
        ttk.Button(frame, text="Browse", command=self.browse_decrypt_file).grid(row=0, column=2)

        ttk.Label(frame, text="Decryption Key:").grid(row=1, column=0)
        self.decrypt_key = tk.StringVar()
        ttk.Entry(frame, textvariable=self.decrypt_key, width=40).grid(row=1, column=1)

        ttk.Button(frame, text="Decrypt Message", command=self.decrypt).grid(row=2, column=1)

        ttk.Label(frame, text="Decrypted Message:").grid(row=3, column=0)
        self.result_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.result_var, state="readonly", width=40).grid(row=3, column=1)

    def encrypt(self):
        img_path = self.src_path.get()
        msg = self.secret_msg.get("1.0", tk.END).strip()

        if not img_path:
            messagebox.showerror("Error", "Select image")
            return
        if not msg:
            messagebox.showerror("Error", "Enter message")
            return

        try:
            img = cv2.imread(img_path)
            key = Fernet.generate_key()
            cipher = Fernet(key)

            encrypted = cipher.encrypt(msg.encode())
            encoded = encrypted.decode()

            length = len(encoded).to_bytes(4, 'big')
            full_msg = ''.join([chr(b) for b in length]) + encoded

            if len(full_msg) > img.shape[0] * img.shape[1]:
                messagebox.showerror("Error", "Too large")
                return

            n, m, z = 0, 0, 0
            for char in full_msg:
                img[n, m, z] = ord(char)
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3

            cv2.imwrite("secret_image.png", img)
            self.key_var.set(key.decode())
            messagebox.showinfo("Success", "Encrypted")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        img_path = self.encrypted_path.get()
        key = self.decrypt_key.get()

        if not img_path or not key:
            messagebox.showerror("Error", "Missing input")
            return

        try:
            img = cv2.imread(img_path)

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

            extracted = []
            for _ in range(length):
                extracted.append(chr(img[n, m, z]))
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3

            cipher = Fernet(key.encode())
            decrypted = cipher.decrypt(''.join(extracted).encode()).decode()
            self.result_var.set(decrypted)
            messagebox.showinfo("Success", "Decrypted")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()