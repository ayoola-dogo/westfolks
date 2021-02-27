import os
from shutil import copy2


def remove_file_dir(file):
    pass


def move_company_image(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_dir = os.path.join(BASE_DIR, 'static/media/default/img/')
    files = os.listdir(image_dir)
    current_user = request.user
    user_destination = os.path.join(BASE_DIR, 'static/media/{}/img/'.format(current_user.email))
    media_root = os.path.join(BASE_DIR, 'static/media')
    for file in files:
        if str(file) != "default.png":
            src = os.path.join(image_dir, file)
            dst = os.path.join(user_destination, file)
            copy2(src, dst)
            os.remove(src)
            return dst


def get_company_image():
    pass
