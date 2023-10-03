from django.shortcuts import render
from example.make_art import convert_image_to_ascii
from .models import RawImage

def home(request):
    """this view is for the root path"""
    
    all_images = RawImage.objects.all()
    print(all_images)

    if request.method == "POST":

        image_pk = request.POST["image_pk"]

        image = RawImage.objects.get(pk=pk)
        image_url = image.get_image

        ascii_image = convert_image_to_ascii(image_url)
        print(image_url)
    else:
        image = None
        ascii_image = None

    context = {
            "all_images": all_images,
            "image": image,
            "ascii_image": ascii_image,
            }

    return render(request, "asciiweb/home.html", context)
