import requests
import base64
import json

class ImageSender():
    def __init__(self, url):
        self.url = url 

    def Send(self, img):
        content_type = 'multipart/form-data'
        data = base64.b64encode(img)
        
        payload = {'image': data}
        
        response = requests.post(self.url, data=payload)
        
        if(response.status_code and response.status_code == 200):
            return True
            
        return False