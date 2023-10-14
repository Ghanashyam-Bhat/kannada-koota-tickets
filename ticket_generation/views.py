from django.http import JsonResponse
import json
from authentication.views import auth
from .models import attendee as Attendee
from django.contrib.auth import get_user_model

# Create your views here.    
def ticketSubmissions(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    data = json.loads(req_body)
    User = get_user_model()
    if status!=200:
        response =  JsonResponse({'message': 'REDIRECT'}, status=500)
        return response
    try:
        if request.method == 'POST':
            newAttendee = Attendee(
                id = data["universityId"],
                email = data["email"],
                name = data["name"],
                phone = data["contact"],
                isCash = True if "Cash"==data["paymentMethod"] else False,
                handledBy = User.objects.get(pk=message["id"])
            )
            newAttendee.save()
            response =  JsonResponse({'message': 'SUCCESS'}, status=200)
    except Exception as err:
        print(f"Server Error in ticket submission.\nRequest -> {request}\nError -> {err}")


