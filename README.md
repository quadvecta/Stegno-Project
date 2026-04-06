
# 🖼️ Image Steganography Project (v2.1 - GUI)

[![Version](https://img.shields.io/badge/version-v2.1-blue.svg)](https://github.com/quadvecta/Stegno-Project/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

# This project has numerous intentional bugs and easters. 
## Any freshmen is welcome to debug and explore. HAPPY LEARNING!!


A Python GUI application to **hide and extract secret messages** within an image using steganography and password protection. This upgraded version features an easy-to-use graphical interface built with Tkinter.

> 💡 Looking for the CLI version? Switch to the `cli-legacy` branch.

---

## ✨ What's New in v2.1
- 🖥️ GUI interface
- 🔐 Secure password encryption using **Fernet**
- 🖼️ Image preview and confirmation
- 🧠 Error handling, key saving, and message validation

---

## 📦 Requirements

Make sure Python is installed (>= 3.6), then install the dependencies:

```bash
pip install opencv-python pillow cryptography
```

No external GUI libraries needed — **Tkinter** is built into standard Python.

---

## 🛠️ How to Use the GUI

### 🧬 Encoding a Message
1. Run the app:
   ```bash
   python stegno_gui.py
   ```
2. Load an image (`.jpg`, `.png`, etc.) using the file picker.
3. Type your secret message in the message box.
4. Click **“Generate Key”** to create an encryption key.
5. Click **“Encode”** – your message is embedded and saved as `secret_image.png`.

### 🔍 Decoding a Message
1. Run the app and load the `secret_image.png`.
2. Paste the **same key** used to encode the message.
3. Click **“Decode”** to reveal the hidden message.

> 🧠 Make sure to save your encryption key! It is required for decryption.

---

## 📁 Project Files

- `stegno_gui.py` – GUI app for encoding/decoding
- `secret_image.png` – Output image with hidden message
- `README.md`, `CHANGELOG.md`

---

## 🕹️ Legacy CLI Version
The original terminal-based version is available in the `cli-legacy` branch:
- [View CLI Version](https://github.com/quadvecta/Stegno-Project/tree/cli-legacy)

---

## 📦 Releases
- **Latest**: [v2.1 – GUI](https://github.com/quadvecta/Stegno-Project/tree/main)
- **Previous**: [v1.0 – CLI](https://github.com/quadvecta/Stegno-Project/tree/cli-legacy)

---

## 🧾 License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

Built with 💙 using Python + OpenCV + Tkinter

