from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json

# Create your views here.
def login_status(request):
    if not request.user.is_authenticated:
        response =  JsonResponse({'message': 'REDIRECT'}, status=501)
        return response
    else:
        response =  JsonResponse({'message': 'SUCCESS'}, status=200)
        return response
    
def login_api(request):    
    req_body = request.body.decode('utf-8')
    req = json.loads(req_body)
    email = req["email"]
    password = req["password"]
    user = authenticate(request, username=email, password=password)

    if user is not None:
        # Authentication successful
        login(request, user)        
        response =  JsonResponse({'message': 'SUCCESS'}, status=201)
        return response   
    else:
        # Authentication failed
        return JsonResponse({'message': 'FAILURE'}, status=401)
    

def logout_api(request):
    if not request.user.is_authenticated:
        response =  JsonResponse({'message': 'REDIRECT'}, status=501)
        return response
    try:
        logout(request)
        response =  JsonResponse({'message': 'SUCCESS'}, status=201)
        return response
    except:
        response = JsonResponse({'message': 'FAILURE'}, status=401)
        return response
    