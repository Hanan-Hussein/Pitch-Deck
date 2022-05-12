import secrets
import os
from PIL import Image
from flask import url_for,current_app

def save_picture(form_picture):
    """
    
    """

    #base of file name
    random_hex= secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex +f_ext

    picture_path=os.path.join(current_app.root_path,'static/profiles',picture_fn)

    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn
def comments_cutter(string_comments):
    """Takes in a string cuts it and returns a list of comments
    """
    return string_comments.split(';')
