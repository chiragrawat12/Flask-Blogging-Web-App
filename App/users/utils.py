import os
from secrets import token_hex
from PIL import Image
from flask import current_app
from flask import url_for
from flask_mail import Message
from App import mail
from flask_login import current_user

def save_picture(form_picture):
    random_hex=token_hex(8)
    _ , f_ext=os.path.splitext(form_picture.filename)
    picture_fn= random_hex + f_ext
    picture_path=os.path.join(current_app.root_path,'static/profile_pic',picture_fn)
    
    output_size=(125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    if current_user.image_file != "default.jpg":
        os.remove(current_app.root_path+"/static/profile_pic/" + current_user.image_file)

    img.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='chiragrawat12@gmail.com',recipients=[user.email])
    msg.body = """ To reset your password, visit the following link:
{}
If you did not make this request then simply please ignore the message and no changes will be made
""".format(url_for('users.reset_token',token=token,_external=True))
    mail.send(msg)
