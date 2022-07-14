import json

def get_data():

    with open('data_j.json') as file:
        data = json.load(file)['content'][0]

    return data

