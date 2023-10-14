from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
from .models import attendee as Attendee

# Create your views here.    
def ticketSubmissions(request):
    if not request.user.is_authenticated:
        response =  JsonResponse({'message': 'REDIRECT'}, status=302)
        return response
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            newAttendee = Attendee(
                id = data["id"],
                email = data["email"],
                name = data["name"],
                phone = data["phone"],
                isCash = data["isCash"],
                handledBy = request.user.name
            )
            newAttendee.save()
    except Exception as err:
        print(f"Server Error in ticket submission.\nRequest -> {request}\nError -> {err}")


