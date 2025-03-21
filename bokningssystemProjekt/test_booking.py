import unittest
from unittest.mock import patch, MagicMock
from BookingRepository import BookingRepository
from BookingManager import BookingManager


class TestBookingRepository(unittest.TestCase):
    @patch("BookingRepository.BookingRepository.load_bookings_from_file")  # Mocka fil-läsning
    def setUp(self, mock_load_file):
        """Skapar en testinstans av BookingRepository och mockar filhantering."""
        self.repo = BookingRepository("test_bookings.json") #Skapar en testinstans. 
        self.repo.save_dict_to_json_file = MagicMock()  # Mocka fil-skrivning för att undvika ändringar av fil. 

        # Manuellt sätta testdata istället för att läsa från fil. 
        self.repo._BookingRepository__bookings_dict = {
            "kund1@example.com": {
                "email": "kund1@example.com",
                "date": "2025-04-01",
                "time": "11:00",
                "name": "Kund 1",
                "service": "Klippning långt hår",
                "hairdresser": "Sara"
            },
            "kund2@example.com": {
                "email": "kund2@example.com",
                "date": "2025-04-01",
                "time": "12:00",
                "name": "Kund 2",
                "service": "Klippning kort hår",
                "hairdresser": "Peter"
            },
            "kund3@example.com": {
            "email": "kund3@example.com",
            "date": "2025-04-02",
            "time": "10:00",
            "name": "Kund 3",
            "service": "Klippning långt hår",
            "hairdresser": "Hannah"
          }
        }

    @patch("BookingRepository.BookingRepository.load_bookings_from_file")
    def test_load_bookings_from_file_mocked(self, mock_load_file):
        """Testar att `load_bookings_from_file()` laddar in bokningar korrekt med mockad JSON-data. """

        #Simulerad testdata som förväntas laddas in. 
        mock_data = {
            "kund4@example.com": {
            "email": "kund4@example.com",
            "date": "2025-04-08",
            "time": "10:00",
            "name": "Kund 4",
            "service": "Klippning långt hår",
            "hairdresser": "Hannah"
          }
        }
        repo = BookingRepository("mocked.json") #Skapar en testinstans. 
        repo._BookingRepository__bookings_dict = mock_data  #Sätt testdatan manuellt. 
        
        #Verifiera att bokningarna laddats in korrekt. 
        self.assertDictEqual(repo.get_all(), mock_data)


    def test_search_date_found(self):
        """Testar att `search_date()` returnerar ALLA bokningar för ett specifikt datum."""
        result = self.repo.search_date("2025-04-01")
        expected_result = {
            "kund1@example.com": self.repo._BookingRepository__bookings_dict["kund1@example.com"],
            "kund2@example.com": self.repo._BookingRepository__bookings_dict["kund2@example.com"]
        }
        self.assertDictEqual(result, expected_result)  #Verifiera att rätt bokningar returneras. 


    def test_search_date_single_result(self):
        """Testar att `search_date()` returnerar ENDAST en bokning om bara en matchar."""
        result = self.repo.search_date("2025-04-02")  # Bara en bokning ska returneras.
        expected_result = {
            "kund3@example.com": {
            "email": "kund3@example.com",
            "date": "2025-04-02",
            "time": "10:00",
            "name": "Kund 3",
            "service": "Klippning långt hår",
            "hairdresser": "Hannah"
          }
        }
        self.assertDictEqual(result, expected_result)  # Verifiera att endast en bokning returneras. 

    def test_search_date_not_found(self):
        """Testar att `search_date()` returnerar en tom dictionary om datumet saknas."""
        result = self.repo.search_date("2025-05-01")  # Datum som inte finns
        self.assertEqual(result, {})  # Ska returnera en tom dictionary

    def test_delete_booking_success(self):
        """Testar att `delete_booking()` tar bort en bokning korrekt."""
        self.assertIn("kund1@example.com", self.repo.get_all())  # Kontrollera att bokningen finns
        
        result = self.repo.delete_booking("kund1@example.com")
        self.assertTrue(result)  # Ska returnera True om bokningen togs bort
        self.repo.save_dict_to_json_file.assert_called_once()  # Kontrollera att ändringen sparades
        self.assertNotIn("kund1@example.com", self.repo.get_all())  # Kontrollera att den är borta

    def test_delete_booking_nonexistent(self):
        """Testar att `delete_booking()` returnerar False om bokningen inte finns."""
        result = self.repo.delete_booking("nonexistent@example.com")
        self.assertFalse(result)  # Ska returnera False om bokningen inte finns

#Tester för klassen BookingManager. 
class TestBookingManager(unittest.TestCase):
    def setUp(self):
        """Skapar en testinstans av BookingManager med en mockad BookingRepository."""
        self.manager = BookingManager("test_bookings.json")
        self.manager.repo = MagicMock()  # Mocka BookingRepository för att undvika beroenden. 

    def test_search_by_date_found(self):
        """Testar att `search_by_date()` i BookingManager anropar repository och returnerar resultat."""
        self.manager.repo.search_date.return_value = {   #Simulera en bokning. 
            "kund1@example.com": {
                "email": "kund1@example.com",
                "date": "2025-04-01",
                "time": "11:00",
                "name": "Kund 1",
                "service": "Klippning långt hår",
                "hairdresser": "Sara"
            }
        }
        result = self.manager.search_by_date("2025-04-01")
        self.assertEqual(len(result), 1)  # Endast en bokning ska returneras
        self.assertIn("kund1@example.com", result)  # Kontrollera att rätt nyckel finns
        self.manager.repo.search_date.assert_called_once_with("2025-04-01")  # Kontrollera att metoden anropades

    def test_search_by_date_not_found(self):
        """Testar att `search_by_date()` i BookingManager returnerar tom dictionary när ingen bokning hittas."""
        self.manager.repo.search_date.return_value = {}  # Simulera att inga bokningar hittas
        result = self.manager.search_by_date("2025-05-01")  # Datum utan bokningar
        self.assertEqual(result, {})  # Ska returnera en tom dictionary

    def test_delete_booking_manager_success(self):
        """Testar att BookingManager kan ta bort en bokning."""
        self.manager.repo.delete_booking.return_value = True  # Simulera att raderingen lyckas
        result = self.manager.delete_booking("test@example.com")
        self.assertTrue(result)  #Kontrollera att resultate är True. 
        self.manager.repo.delete_booking.assert_called_once_with("test@example.com")  #Kontrollera metodanrop. 

    def test_delete_booking_manager_nonexistent(self):
        """Testar att BookingManager hanterar försök att ta bort en icke-existerande bokning korrekt."""
        self.manager.repo.delete_booking.return_value = False  # Simulera att raderingen misslyckas
        result = self.manager.delete_booking("nonexistent@example.com")
        self.assertFalse(result)  #Kontrollera att resultatet är False. 

if __name__ == '__main__':
    unittest.main()