import requests
import json

def weekday_choices():
    data  = requests.get("http://34.70.184.173:8000/user/prefstyleimages/")
    data = data.json()
    data_choices = data.get('Response')
    choices = []
    for choice in data_choices:
        if(choice['style']=='Weekday'):
            Help = [] 
            Help.append(choice['id'])
            Help.append(choice['image'])
            choices.append(tuple(Help)) 
    return(choices)

def weekend_choices():
    data  = requests.get("http://34.70.184.173:8000/user/prefstyleimages/")
    data = data.json()
    data_choices = data.get('Response')
    choices = []
    for choice in data_choices:
        if(choice['style']=='Weekend'):
            options = [] 
            options.append(choice['id'])
            options.append(choice['image'])
            choices.append(tuple(options)) 
    return(choices)

def brand_choices():
    data  = requests.get("http://34.70.184.173:8000/user/prefbrandimages/")
    data = data.json()
    data_choices = data.get('Response')
    choices = []
    for choice in data_choices:
        options = [] 
        options.append(choice['brand_id'])
        options.append(choice['image'])
        choices.append(tuple(options)) 
    print(choices)
    return(choices)

def string_id(varids,var):
    stringid = []
    for varid in varids:
        string = var +str(varid)
        print(string)
        stringid.append(string)
    string = ', '.join(stringid)
    return (string)
        
def user_preferences(form):
    request = {}
    request["user_id"] = "4"
    request["gender"] = form.get('gender')
    request["dob"] = "2018-12-12"
    request["workstyles"] = string_id(form.get('weekday_style'),"id")
    request["weekendstyles"] = string_id(form.get('weekend_style'),"id")
    request["brands"] = string_id(form.get('brand'),"brandid")
    print(json.dumps(request))
    #error
    data = requests.api.post("http://34.70.184.173:8000/user/userpref/", json=request) 
    print(data.json())
    return 