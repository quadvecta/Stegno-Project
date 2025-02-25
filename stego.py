import cv2
import os
import base64
from cryptography.fernet import Fernet
import numpy as np


image_path = r"D:\Programming\VS Code\Python\image.jpg" # Make sure to change the file location of the image!


if not os.path.exists(image_path):
    print("Error: Image file not found at", image_path)
    exit()


img = cv2.imread(image_path)
if img is None:
    print("Error: Failed to load the image. Check file format or permissions.")
    exit()


key = Fernet.generate_key()
cipher = Fernet(key)

print("\n[NOTE] Keep this decryption key safe: ", key.decode())


msg = input("Enter secret message: ")
password = input("Enter a passcode: ")


encrypted_msg = cipher.encrypt(msg.encode())  
encoded_msg = base64.b64encode(encrypted_msg).decode()  


height, width, _ = img.shape
if len(encoded_msg) > height * width:
    print("Error: Message too long to fit in the image.")
    exit()


n, m, z = 0, 0, 0
for char in encoded_msg:
    img[n, m, z] = ord(char)  
    m += 1
    if m >= width:
        m = 0
        n += 1
    z = (z + 1) % 3  

cv2.imwrite("encryptedImage.jpg", img)
os.system("start encryptedImage.jpg")  

# Decryption Process
print("\n--- Decryption Process ---")
decryption_key = input("Enter the decryption key: ")

if decryption_key.encode() == key: 
    n, m, z = 0, 0, 0
    extracted_chars = []
    
    for _ in range(len(encoded_msg)):
        extracted_chars.append(chr(img[n, m, z])) 
        m += 1
        if m >= width:
            m = 0
            n += 1
        z = (z + 1) % 3
    
    
    extracted_text = "".join(extracted_chars)
    decrypted_msg = cipher.decrypt(base64.b64decode(extracted_text)).decode()

    print("Decrypted Message:", decrypted_msg)
else:
    print("ERROR: Incorrect decryption key. Access Denied!")
