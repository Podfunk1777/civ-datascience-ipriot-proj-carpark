import carpark_manager
import unittest

class TestParkingLot(unittest.TestCase):
    def test_no_negative_spaces(self):
        '''Test case to see if carpark allows for negative spaces or not

        Current implementation of available spaces relies on a list of car objects
        '''
        test_list = []
        for i in range(1, 131):
            test_list.append(carpark_manager.Car(str(i)))
        parking_lot = carpark_manager.CarparkManger()
        parking_lot.list_of_cars = test_list
        parking_lot.incoming_car("TEST1")
        parking_lot.incoming_car("TEST2")
        self.assertEqual(parking_lot.available_spaces, 0)
        parking_lot.outgoing_car("TEST1")
        parking_lot.outgoing_car("TEST2")
        parking_lot.outgoing_car("1")
        self.assertEqual(parking_lot.available_spaces, 1)

    def test_duplicate_license_plates(self):
        #Test case to see if carpark manger can handle duplicate license plates in some way
        parking_lot = carpark_manager.CarparkManger()
        parking_lot.incoming_car("TEST")
        parking_lot.incoming_car("TEST")
        parking_lot.outgoing_car("TEST")
        self.assertEqual(parking_lot.available_spaces, 129)

if __name__ == '__main__':
    unittest.main()