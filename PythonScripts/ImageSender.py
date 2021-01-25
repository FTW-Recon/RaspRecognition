import requests
import json


class ImageSender():
    def __init__(self, url):
        self.url = url 

    def send(self, img, names):
        
        payload = {'data': img, 'pessoas': names}
        print(type(img))
        payload = json.dumps(payload)
        headers = {'Content-Type':'application/json'}
        re = requests.post(self.url, headers=headers, data=payload)
        print(re.status_code)
        if(re.status_code and re.status_code == 200):
            return True
            
        return False