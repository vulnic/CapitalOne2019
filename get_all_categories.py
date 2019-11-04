import requests
import json

def get_categories(num_cat,offset):
    url = 'http://jservice.io/api/categories'

    response = requests.get(url, params = {'count':num_cat, 'offset':offset})

    return response.json()

#THERE ARE 18415 categories!!!!!
""" 
my_list = []

for i in range(185): #should be 185
    if(i%10 == 0):
        print(i)

    my_list += get_categories(100,i*100)

with open('data.json', 'w') as f:
    json.dump(my_list, f)

print(len(my_list)) 

with open('data.json', 'r') as f:
    my_list = json.load(f)
    for item in my_list:
        if(item['title'] == "potpourriiii" or item['title'] == "stupid answers" or item['title'] == "sports" or item['title'] == "american history" or item['title'] == "animals"):
            print("HITT! " + item['title'] + ", id = " + str(item['id'])) """


with open('data.json', 'r') as f:
    my_list = json.load(f)
    