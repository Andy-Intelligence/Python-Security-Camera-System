
import os
import threading
import requests
from dotenv import load_dotenv
import cloudinary
from cloudinary.uploader import upload


load_dotenv()



          
cloudinary.config( 
  cloud_name = os.getenv("cloud_name"), 
  api_key = os.getenv("api_key"), 
  api_secret = os.getenv("api_secret") 
)




API_ENDPOINT = "http://127.0.0.1:5000/motion-detected"


def cloudinary_video_upload(video_file_path):
    response = upload(video_file_path,resource_type="auto")

    url = response['secure_url']
    print(f"File {video_file_path} uploaded to CLOUDINARY in bucket.")
    return url



#this function converts a video format to format accessible by browsers and uploads 
#it to google cloud storage and returns a url but the process will be done in a thread to avoid interfernce
def handle_detection(video_path):
    def convert_video_and_upload(video_path):
        url = cloudinary_video_upload(video_path,)

        data = {
            "url":url
        }

        requests.post(API_ENDPOINT, json=data)

    thread = threading.Thread(target=convert_video_and_upload,args=(video_path,))
    thread.start()

    



