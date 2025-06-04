import requests
import time
from datetime import datetime
#import os

#folder_path = "C:\\Users\\svenc\\Documents\\Pytorch\\oostende"
#os.makedirs(folder_path, exist_ok=True)  # Creates folder if it doesn't exist


# Direct webcam image URL
image_url = "https://www.meteobelgium.net/webcam_other/ostende2/photo.jpg"

def save_image():
    response = requests.get(image_url)
    if response.status_code == 200:
        filename = f"C:\\Users\\svenc\\Documents\\Pytorch\\oostende\\wave_{datetime.now().strftime('%Y%m%d_%H%M')}.jpg"
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Saved: {filename}")
    else:
        print("Failed to download image.")

# Run script every 15 minutes
while True:
    save_image()
    time.sleep(900)  # 900 seconds = 15 minutes


#import requests
#from datetime import datetime

#image_url = "https://www.meteobelgium.net/webcam_other/ostende2/photo.jpg"
#save_path = f"C:\\temp\\pictures\\wave_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

#response = requests.get(image_url)
#if response.status_code == 200:
 #   with open(save_path, "wb") as file:
  #      file.write(response.content)
   # print(f"Saved: {save_path}")
#else:
 #   print("Failed to download image.")
