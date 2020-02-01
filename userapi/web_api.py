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