from faker import Faker
import random
import time

fake = Faker()

def generate_fake_flight_number():
    airline_code = fake.random_uppercase_letter() + fake.random_uppercase_letter()
    flight_number = fake.random_int(min = 1000, max = 9999)

    return f"{airline_code}{flight_number}"

class Airplane:
    def __init__(self, flightID, priority) -> None:
        self.flightID = flightID
        self.priority = priority
        self.next = None
        self.prev = None 


class Takeoff:
    def __init__(self) -> None:
        self.queue = []
        self.priorityCounter = 0

    def insert(self, flightID):
        airplane = Airplane(str(flightID), self.priorityCounter)
        self.queue.append(airplane)
        self.priorityCounter += 1

    def successful(self):
        if not self.queue_is_empty():
            completed_flight = self.queue[0]
            self.queue.pop(0)
            self.decrease_priority()
            print(f"Takeoff successful for Flight {completed_flight.flightID}")

    def queue_is_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False
        
    def decrease_priority(self):
        for airplane in self.queue:
            airplane.priority -= 1
    
    def display_queue(self):
            for takeoff in self.queue:
                print(f"Flight {takeoff.flightID}")
        


class Landing:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def insert(self, flightID, priority=0):
        airplane = Airplane(str(flightID), priority)
        if priority > 0:
            # Emergency landing
            if self.head is None:
                self.head = airplane
                self.tail = airplane
            else:
                iter = self.head
                while iter is not None and iter.priority > 0:
                    iter = iter.next
                if iter is None:
                    self.tail.next = airplane
                    airplane.prev = self.tail
                    self.tail = airplane
                else:
                    airplane.next = iter
                    airplane.prev = iter.prev
                    if iter.prev:
                        iter.prev.next = airplane
                    else:
                        self.head = airplane
                    iter.prev = airplane
        else:
            # Regular landing
            if self.head is None:
                self.head = airplane
                self.tail = airplane
            else:
                self.tail.next = airplane
                airplane.prev = self.tail
                self.tail = airplane

    def successful(self):
        if self.head is not None:
            completed_flight = self.head
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None
            print(f"Landing successful for Flight {completed_flight.flightID}")

    def queue_is_empty(self):
        return self.head is None

    def display_queue(self):
        iter = self.head
        while iter is not None:
            print(f"Flight {iter.flightID} - Priority: {iter.priority}")
            iter = iter.next




if __name__ == "__main__":
    landing = Landing()
    takeoff = Takeoff()

    
    while True:

        time.sleep(1) #Time sleeps are used to simulate more realistic time pass.

        print("\nLanding queue:")
        landing.display_queue()

        print("\nTakeoff queue:")
        takeoff.display_queue()
        time.sleep(1)

        action1 = random.choice(['Landing', 'Takeoff']) #Randomly generating a request to land or takeoff.
        if action1 == 'Landing':
            flight_number = generate_fake_flight_number()
            landing.insert(flight_number, random.choices([0, 1], weights=[0.95, 0.05])[0]) #The landings have a 95% chance of having a regular landing, while 5% of them have an emergency landing.
            print(f"\nFlight {flight_number} requesting landing clearance.")
            action2 = random.choice(['Wait', 'Land']) #Randomly choosing to let the landing proceed or wait (mostly to have a chance to populate the landing queue).
            if action2 == 'Land':
                print(f"Flight {flight_number} cleared for landing.")
                landing.successful()
            else:
                print(f"Flight {flight_number} waiting for clearance to land.")
           

        else:
            flight_number = generate_fake_flight_number()
            takeoff.insert(flight_number)
            print(f"\nFlight {flight_number} requesting takeoff clearance.")
            if landing.queue_is_empty():
                print(f"Flight {flight_number} cleared for takeoff.")
                takeoff.successful()
            else:
                print(f"Flight {flight_number} waiting for clearance to takeoff.")


        endDay = input("Want to end the day? (Type Y for yes or N for no): ") #Completes the remaining flights without populating any of the queues.
        if endDay == 'Y':
            while True:
                if not landing.queue_is_empty():
                    landing.successful()
                    time.sleep(1)
                else:
                    break
            while True:
                if not takeoff.queue_is_empty():
                    takeoff.successful()
                    time.sleep(1)
                else:
                    break
            break            



        