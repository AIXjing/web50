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