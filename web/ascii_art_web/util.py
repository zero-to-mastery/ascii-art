def allowed_image(filename):
    # accept only files with .ext
    if '.' not in filename:
        return False

    # accept only .png or .jpg file extensions
    ext = filename.rsplit('.', 1)[1]
    if not ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return False
    return True


def allowed_image_size(filesize):
    if not int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return False
    return True
