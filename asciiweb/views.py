from django.shortcuts import render

def home(request):
    """this view is for the root path"""

    return render(request, "asciiweb/home.html", {})
