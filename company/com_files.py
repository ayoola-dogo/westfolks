import os
from shutil import copy2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def change_image_path(image):
    filename = os.path.split(image)[1]
    dir_path = os.path.split(image)[1]
    return dir_path, filename


def remove_file_dir(file):
    pass


def move_company_image(request):
    image_dir = os.path.join(BASE_DIR, 'static/media/default/img/')
    files = os.listdir(image_dir)
    current_user = request.user
    user_destination = os.path.join(BASE_DIR, 'static/media/{}/img/logo/'.format(current_user.email))
    for file in files:
        if str(file) != "default.png":
            src = os.path.join(image_dir, file)
            dst = os.path.join(user_destination, file)
            copy2(src, dst)
            os.remove(src)


def get_company_logo(model, user_email):
    media_root = os.path.join(BASE_DIR, 'static/media/')
    new_path = os.path.join(media_root, '{}/img/logo/'.format(user_email))
    dir_path, filename = change_image_path(model.get_logo_url())
    print(os.path.join(new_path, filename))
    return os.path.join(new_path, filename)


def get_logo_url(model, user_email):
    logo_url = '{}/img/logo/'.format(user_email)
    dir_path, filename = change_image_path(model.get_logo_url())
    print(os.path.join(logo_url, filename))
    return os.path.join(logo_url, filename)
