from django.http import JsonResponse
import json
from authentication.views import auth
from ticket_generation.addToFirebase import addToFirebase
from .models import attendee as Attendee
from django.contrib.auth import get_user_model
from ticket_generation.generateUniqueCode import generateUniqueData
from ticket_generation.sendMail import sendMail
import datetime


# Create your views here.
def ticketSubmissions(request):
    req_body = request.body.decode("utf-8")
    message, status = auth(req_body=req_body)
    data = json.loads(req_body)
    User = get_user_model()
    if status != 200:
        response = JsonResponse({"message": "REDIRECT"}, status=401)
        return response
    try:
        response = JsonResponse({"message": "SUCCESS"}, status=201)
        if request.method == "POST":
            data["universityId"] = data["universityId"].strip()
            hash_val = generateUniqueData(
                data["universityId"], data["email"], data["name"], data["contact"]
            )
            handler = User.objects.get(pk=message["id"])
            count = Attendee.objects.count()
            # Storing data in Postgress
            try:
                attendeeData = Attendee.objects.get(id=data["universityId"].upper())
                hash_val = attendeeData.hashVal
                newAttendee = Attendee(
                    id=data["universityId"].upper(),
                    email=data["email"].lower(),
                    name=data["name"].title(),
                    phone=data["contact"],
                    isCash=True if data["paymentMethod"] == "Cash" else False,
                    handledBy=handler,
                    hashVal=hash_val,
                    isVip=True if data["ttype"] == "VIP" else False,
                    created_datetime=(
                        datetime.datetime.now()
                        + datetime.timedelta(hours=5, minutes=30)
                    ).isoformat(" "),
                    mailid=(count + 1) % 5,
                )
                newAttendee.save()
                response = JsonResponse({"message": "Data already exists"}, status=200)
            except:
                newAttendee = Attendee(
                    id=data["universityId"].upper(),
                    email=data["email"].lower(),
                    name=data["name"].title(),
                    phone=data["contact"],
                    isCash=True if data["paymentMethod"] == "Cash" else False,
                    handledBy=handler,
                    hashVal=hash_val,
                    isVip=True if data["ttype"] == "VIP" else False,
                    created_datetime=(
                        datetime.datetime.now()
                        + datetime.timedelta(hours=5, minutes=30)
                    ).isoformat(" "),
                    mailid=(count + 1) % 5,
                )
                newAttendee.save()
                response = JsonResponse({"message": "SUCCESS"}, status=201)
            try:
                sendMail(
                    newAttendee.id,
                    newAttendee.email,
                    newAttendee.name,
                    newAttendee.phone,
                    newAttendee.hashVal,
                    newAttendee.isVip,
                    newAttendee.mailid,
                )
                try:
                    # Storing data in firebase
                    data = {
                        "id": data["universityId"].upper(),
                        "email": data["email"].lower(),
                        "name": data["name"].title(),
                        "phone": data["contact"],
                        "isCash": True if "Cash" == data["paymentMethod"] else False,
                        "handledBy": handler.get_username(),
                        "hashVal": hash_val,
                        "verified": False,
                        "isVip": True if data["ttype"] == "VIP" else False,
                    }
                    addToFirebase(data)
                except Exception as e:
                    print("ERROR -> Failed to add data to firebase:", e)
                    response = JsonResponse(
                        {"message": "Failed to add data to firebase"}, status=500
                    )
                    return response
            except Exception as e:
                print("Error -> Failed to send email:", e)
                response = JsonResponse({"message": "Email Failed"}, status=500)
                return response
            return response
    except Exception as err:
        print(
            f"Server Error in ticket submission.\nRequest -> {request}\nError -> {err}"
        )
        response = JsonResponse({"message": "ERROR"}, status=500)
        return response
