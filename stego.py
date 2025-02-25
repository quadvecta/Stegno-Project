import cv2
import os


image_path = r"D:\Programming\VS Code\Python\image.jpg" # Make sure to change the file location!

if not os.path.exists(image_path):
    print("Error: Image file not found at", image_path)
    exit()

img = cv2.imread(image_path)

if img is None:
    print("Error: Failed to load the image. Check file format or permissions.")
    exit()

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

d = {chr(i): i for i in range(256)} 
c = {i: chr(i) for i in range(256)}

height, width, _ = img.shape

n = 0
m = 0
z = 0


if len(msg) > height * width:
    print("Error: Message too long to fit in the image.")
    exit()


for i in range(len(msg)):
    img[n, m, z] = d[msg[i]]
    m += 1
    if m >= width:  
        m = 0
        n += 1
    z = (z + 1) % 3  

cv2.imwrite("encryptedImage.jpg", img)
os.system("start encryptedImage.jpg")  # Open image on Windows using "start"


message = ""
n = 0
m = 0
z = 0

pas = input("Enter passcode for decryption: ")

if password == pas:
    for i in range(len(msg)):
        message += c[img[n, m, z]]
        m += 1
        if m >= width:
            m = 0
            n += 1
        z = (z + 1) % 3
    print("Decryption message:", message)
else:
    print("ERROR: Incorrect passcode. You are not authorized!")
