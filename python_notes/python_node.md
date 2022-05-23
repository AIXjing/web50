## Variables

```py
a = 28  # int
b = 1.5  # float
c = "Hello"  # str
d = True  # bool
e = None  # NoneType
```

## Input/Output

```py
name = input("Name: ")
print("Name, ", name);

print(f"Hello, {name}")  # formatted print
```

## Conditions

```py
n = int(input("Number: "))

if n > 0:
    print("n is positive")
elif n < 0:
    print("n is negative")
else:
    print("n is zero")
```

## Sequences

1. String

    ```py
    name = "Harry"
    print(name[0]) # output: H
    ```

2. List - a sequence of mutable values

    ```py
    names = ["Harry", "Maria", "Mike"]
    print(names[0])  # output: Harry

    names.append("Ginny")
    names.sort()
    ```

3. Tuple - a sequence of immutable values

    - store several variables together

    ```py
    coordiante = (10.0, 20.0)
    ```

4. Set - collection of unique values

    ```py
        # create a set
        s = set()
        # add element to set
        s.add(1)
        s.add(2)
        print(s)
        # output: {1,2}

        s.add(2)
        print(s)
        # output: {1,2}

        s.remove(2)
        len(s) # tells the set length

    ```

5. Dict - collection of key-value paris

    ```py
    houses = {"Harry": "G", "Draco": "S"}
    print(houses["Harry"]) # output: G

    # add element to a dictionary
    houses["Hermione"] = "G"
    ```

## Loops

```py
    for i in range(6): # [0,1,2,3,4,5]
        print(i)

    name = "Harry"
    for c in name:
        print(c)
```

## Functions

```py
def square(x):
    return x * x

# implement the function
for i in range(10):
    print(f"Square of {i} is {square(i)}")
```

if the function is from other file, use `from <filename> import <function>`. We could also import `csv` file if needed. 

## Object-Oriented Programming

```py
# create a class
class Point():
    def __init__(self, input_x, input_y): # equivalent to constructor in Java
        self.x = input_x  # parse input_x to x
        self.y = input_y  # parse input_y to y


p = Point(1,5)
print(p.x)
print(p.y)
```

One more example:

```py
class Flight():
    def __init__(self, input):
        self.capacity = input
        self.passengers = []

    # add a new passenger to the passengers
    def add_passenger(self, name):
        if not self.open_seats():
            return False
        self.passengers.append(name)
        return True

    def open_seats(self):
        return self.capacity - len(self.passengers)


flight = Flight(3)

people = ["Harry", "Jane", "Mike", "Ann"]

for person in people:
    success = flight.add_passenger(person)
    if success:
        print(f"Successfully add {person}")
    else:
        print(f"No available searts for {person}")
```

## Decorator

Pass a function to another function as an input - *Functional programming*

```py
def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done with the function")
    return wrapper


@announce
def hello():
    print("Hello, world!")

hello()
```

## lambda

```py
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
```

## Handling exception

use `try`/`except`

```py
import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Error: Invalid input.")
    sys.exit(1)

try:
    result = x / y
except ZeroDivisionError:
    print("Error: Cannot divide by 0.")
    sys.exit(1)

print(f"{x} / {y} = {result}.")
```


