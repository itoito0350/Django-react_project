from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Bienvenido a la API del Gimnasio"}, status=200)
