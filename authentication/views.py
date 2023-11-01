from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse, HttpResponse
import json
import http
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

# Create your views here.
def auth(req_body):
    try:
        req = json.loads(req_body)
        cookie = req["cookies"]
        session_key = cookie.split("=")[1]
        print(session_key)
    except:
        return {'message': 'FAILURE'},401
        
    User = get_user_model()
    try:
        session = Session.objects.get(session_key=session_key)
        user_id = session.get_decoded().get('_auth_user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            print("user:",user)
            if user.is_authenticated and user.is_active:   
                return {'message': 'SUCCESS','id':user_id},200
        return {'message': 'FAILURE'},401
    except Session.DoesNotExist:
        return {'message': 'FAILURE'},401
    
def login_status(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    return JsonResponse(message,status=status)
    
def login_api(request):    
    req_body = request.body.decode('utf-8')
    req = json.loads(req_body)
    print(req)
    email = req["email"]
    password = req["password"]
    user = authenticate(request, username=email, password=password)
    try:
        if user is not None:
            # Authentication successful
            login(request, user)        
            response =  JsonResponse({'message': 'SUCCESS'}, status=201)
            return response   
        else:
            # Authentication failed
            return JsonResponse({'message': 'FAILURE'}, status=401)
    except Exception as e:
        print("Error:",e)
        return JsonResponse({'message': 'FAILURE'}, status=501)
    
def logout_api(request):
    req_body = request.body.decode('utf-8')
    try:
        req = json.loads(req_body)
        cookie = req["cookies"]
        session_key = cookie.split("=")[1]
    except:
        return JsonResponse({'message': 'FAILURE'}, status=401)
    
    User = get_user_model()
    try:
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        
        if user_id:
            user = User.objects.get(pk=user_id)
            if user.is_authenticated:
                # Clear the session data to mark the user as unauthenticated
                session_data['_auth_user_id'] = None
                session_data['_auth_user_backend'] = ''
                session_data['_auth_user_hash'] = ''
                session.session_data = session_data
                session.save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'FAILURE'}, status=401)
    except Session.DoesNotExist:
        return JsonResponse({'message': 'FAILURE'}, status=401)
    

def proxy_handler(request,*args):
    if request.method == 'GET':
        # Specify the target server and path
        remaining_path = request.path.replace('/proxy', '')

        # Specify the target server and path
        target_host = request.get_host()
        target_path = remaining_path
        
        connection = http.client.HTTPSConnection(target_host)
        # Send a GET request to the target server
        connection.request('GET', target_path)

        # Get the response from the target server
        response = connection.getresponse()
        response_body = response.read().decode('utf-8')
        response_data = json.loads(response_body)
        message = json.dumps(response_data)
        # Close the connection to the target server
        connection.close()
        return HttpResponse(message, content_type='application/json')

    elif request.method == 'POST':
        # Specify the target server and path
        remaining_path = request.path.replace('/proxy', '')

        # Specify the target server and path
        target_host = request.get_host()
        target_path = remaining_path

        # Extract the POST data from the request
        content_length = int(request.META['CONTENT_LENGTH'])
        post_data = request.body.decode('utf-8')

        # Create a connection to the target server
        connection = http.client.HTTPSConnection(target_host)

        # Set the headers for the POST request
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': content_length
        }

        # Send a POST request to the target server
        connection.request('POST', target_path, body=post_data, headers=headers)

        # Get the response from the target server
        response = connection.getresponse()
        response_body = response.read().decode('utf-8')
        response_data = json.loads(response_body)
        
        # Close the connection to the target server
        connection.close()
        
        # Extract the cookie from the response
        if response.status == 201:
            try:
                cookie = response.headers['Set-Cookie'].split(";")[0]
                cookie = cookie.split("=")
                key = cookie[0]
                value = cookie[1]
                response_data[key] = value
                return JsonResponse(response_data,status=201)
            except:
                print("No Cookie Infotmation")
                pass
        return JsonResponse(response_data,status=401)