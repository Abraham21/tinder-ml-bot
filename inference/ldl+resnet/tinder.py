import pynder
import sys
import os
import traceback
import logging
from beauty_predict import want_to_like
from skimage.io import imread, imsave, imshow, show, imsave

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(APP_ROOT)
parent_path = os.path.dirname(parent_path)

facebook_auth_token = "TOKEN_HERE" 
session = pynder.Session(facebook_auth_token) #kwarg
counter = 80
while True:
  try:
    print("Fetching users...")
    users = session.nearby_users()
    for user in users:
        photos = user.get_photos()
        name = user.name
        # Fetch user profile picure
        image = imread(next(photos))
        imsave(parent_path + "/samples/image/tinder" + str(counter) + ".jpg", image)
        # image saved
        like = want_to_like("tinder" + str(counter) + ".jpg")
        if like:
          user.like()
          print("You liked " + name)
        else:
          user.dislike()
          print("You disliked " + name)
        counter = counter + 1
  except Exception as e:
    logging.error(traceback.format_exc())
