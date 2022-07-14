import json

def find_Animal(name_of_animal):

    with open("data_j.json") as file:
        data = json.load(file)['content']

    for animal in data:
        if name_of_animal==animal['animalName']:
            return animal
