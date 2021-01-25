from ImageSender import ImageSender

if __name__ == "__main__":
    
    img = open('imgs/img.jpg', 'rb').read()
    url = 'http://localhost:8000/ImageUpload/'

    img_sender = ImageSender(url)
    sent = img_sender.Send(img)

    if(sent):
        pass
    else:
        pass
    