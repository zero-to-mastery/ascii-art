from django.http import JsonResponse

# Create your views here.
def home(request):
    return JsonResponse({'info': 'Ascii Art Server', 'name': 'ZTM'})