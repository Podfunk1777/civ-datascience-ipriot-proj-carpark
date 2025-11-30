from interfaces import CarparkDataProvider
from interfaces import CarparkSensorListener
from config_parser import parse_config
import time

class CarparkManger(CarparkSensorListener, CarparkDataProvider):
    #constant, for where to get the configuration data
    CONFIG_FILE = "samples_and_snippets\config.json"

    #Set with the assumption that the config file would have a standard format:
    def __init__(self, config=parse_config(CONFIG_FILE), list_of_cars=[], log_contents="", log_filename="carpark_log.txt",temperature_log=[0]):
        '''Carpark constructor

        Creates log file upon initialisation and reads a config file

        '''
        self.config = config
        self.list_of_cars = list_of_cars
        self.temperature_log = temperature_log
        self.log_filename = log_filename
        self.log_contents = log_contents
        self.create_log_file()

    @property
    def available_spaces(self):
        max_space = self.config["total-spaces"]
        available_space = max_space - len(self.list_of_cars)
        if available_space < 0:
            return 0
        else:
            return available_space

    @property
    def temperature(self):
        return self.temperature_log[-1]

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self,license_plate):
        '''Logs incoming cars and at what time

        Params
        ----------
        license_plate : str
            license plate from sense data
        '''
        new_car = Car(license_plate, time.asctime(time.localtime()))
        self.list_of_cars.append(new_car)
        self.log_append(f"Car with license plate {new_car.LicensePlate} has entered at {new_car.entry_time}")
        
        print('Car in! ' + license_plate)

    #Current known issues: will delete all entries of duplicate license plates

    def outgoing_car(self, license_plate):
        '''Logs outgoing cars and at what time. Deletes record of car when called.

        Params
        ----------
        license_plate : str
            license plate from sense data
        '''
        for car in self.list_of_cars:
            if car.LicensePlate == license_plate:
                car.exit_time = time.asctime(time.localtime())
                self.log_append(f"Car with licence plate {car.LicensePlate} has left at {car.exit_time}")
                self.list_of_cars.remove(car)
                break


    def temperature_reading(self, reading):
        '''Thrown together temperature reading thingo that I could spend more time on

        Params
        ----------
        reading : float
            temperature sense data
        '''
        self.log_append(f"New temperature reading: {reading}")
        self.temperature_log.append(reading)
        print(f"temperature is {reading}")

        return reading

    def create_log_file(self):
        #Creates log file (txt format) upon object instantiation
        with open(self.log_filename, 'w') as f:
            f.write(self.log_contents + "\n")

    def log_append(self, new_logs):
        '''Adds any new events to existing log file

        Params
        ----------
        new_logs : str
            Strings to add to log file
        '''
        with open(self.log_filename, 'a') as f:
            f.write(new_logs + "\n")



class Car:
    def __init__(self,plate=None, entry_time="", exit_time=""):
        self.LicensePlate = plate
        self.entry_time = entry_time
        self.exit_time = exit_time