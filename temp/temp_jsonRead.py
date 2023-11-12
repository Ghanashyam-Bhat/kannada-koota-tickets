import json

with open("attendeeData.json") as data:
    jsonData = json.load(data)
    vip_cash = 0
    ga_cash = 0
    vip_online = 0
    ga_online = 0
    for i in jsonData:
        if i["isCash"] == True:
            if i["isVip"] == True:
                vip_cash += 1
            else:
                ga_cash += 1
        else:
            if i["isVip"] == True:
                vip_online += 1
            else:
                ga_online += 1

    print("VIP CASH:", vip_cash)
    print("GENERAL CASH:", ga_cash)
    print("VIP ONLINE:", vip_online)
    print("GENERAL ONLINE:", ga_online)
