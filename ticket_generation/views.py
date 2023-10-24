from django.http import JsonResponse
import json
from authentication.views import auth
from ticket_generation.addToFirebase import addToFirebase
from .models import attendee as Attendee
from django.contrib.auth import get_user_model
from ticket_generation.generateUniqueCode import generateUniqueData
from ticket_generation.sendMail import sendMail

# Create your views here.    
def ticketSubmissions(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    data = json.loads(req_body)
    User = get_user_model()
    if status!=200:
        response =  JsonResponse({'message': 'REDIRECT'}, status=401)
        return response
    try:
        if request.method == 'POST':
            hash_val = generateUniqueData(data["universityId"],data["email"],data["name"],data["contact"])
            handler = User.objects.get(pk=message["id"])
            # Storing data in Postgress
            newAttendee = Attendee(
                id = data["universityId"],
                email = data["email"],
                name = data["name"],
                phone = data["contact"],
                isCash = True if "Cash"==data["paymentMethod"] else False,
                handledBy = handler,
                hashVal = hash_val
            )
            newAttendee.save()
            try:
                sendMail(data["universityId"],data["email"],data["name"],data["contact"],hash_val)
            except Exception as e:
                print("Error -> Failed to send email:",e)
                response =  JsonResponse({'message': 'Email Failed'}, status=200)
                return response
            finally:
                try:
                    # Storing data in firebase
                    data = {
                        "id" : data["universityId"],
                        "email" : data["email"],
                        "name" : data["name"],
                        "phone" : data["contact"],
                        "isCash" : True if "Cash"==data["paymentMethod"] else False,
                        "handledBy" : handler.get_username(),
                        "hashVal" : hash_val
                    }
                    addToFirebase(data)
                except Exception as e:
                    print("ERROR -> Failed to add data to firebase:",e)
                    response =  JsonResponse({'message': 'Failed to add data to firebase'}, status=200)
                    return response
            response =  JsonResponse({'message': 'SUCCESS'}, status=201)
            
            return response
    except Exception as err:
        print(f"Server Error in ticket submission.\nRequest -> {request}\nError -> {err}")
        response =  JsonResponse({'message': 'ERROR'}, status=500)
        return response