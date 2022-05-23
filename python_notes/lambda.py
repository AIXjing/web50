people = [
    {'name': 'Harry', 'house': 'Gruffindor'}, 
    {'name': 'Cho', 'house': 'Ravenclaw'}, 
    {'name': 'Draco', 'house': 'Slytherin'}
]

# to sort list element by name
def f(person):
    return person["name"]

people.sort(key=f)

# using lambda
people.sort(key=lambda person:person["name"])

print(people)