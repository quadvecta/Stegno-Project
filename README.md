# **Image Steganography Project**  

A Python script to hide and extract secret messages within an image. The project includes:  
- A `stego.py` script for steganography  
- An encrypted output image (`encryptedImage.jpg`)   

## **Project Overview**  
Steganography is the practice of hiding information within digital media. This project uses OpenCV to embed a secret message into an image by modifying pixel values.  

## **Requirements**  
Ensure you have Python installed along with the required libraries:  
```bash
pip install opencv-python
```

## **How to Use**  
### **1. Encoding a Message**
1. Place an image (`your_image_file`) in the same directory as `stego.py`.  
2. Run the script:  
   ```bash
   python stego.py
   ```
3. Enter your secret message when prompted.  
4. Set a password for decryption.  
5. The script will generate `encryptedImage.jpg` with the hidden message.  

### **2. Decoding the Message**
1. Run the script again:  
   ```bash
   python stego.py
   ```
2. Enter the correct password.  
3. If correct, the hidden message will be revealed.  

## **Project Files**  
- `stego.py` – Python script for encoding/decoding messages in an image.  
- The original image (not included in the repo).  
- `encryptedImage.jpg` – The image with the hidden message.   
