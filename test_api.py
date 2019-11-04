import requests
import json

def display_clue(user_val, user_cat):
    url = 'http://jservice.io/api/clues'

    response = requests.get(url, params= {'value':user_val, 'category':user_cat, 'offset':0})

    assert response.status_code == 200
    return response.json()

def get_categories(num_cat):
    url = 'http://jservice.io/api/categories'

    response = requests.get(url, params = {'count':num_cat})

    return response.json()

def get_random(user_cat):
    url = 'http://jservice.io/api/random'

    response = requests.get(url, params = {'count':100, 'offset':1000})
    return response.json()


