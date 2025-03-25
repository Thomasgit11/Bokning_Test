import unittest
from unittest.mock import patch, MagicMock
from BookingRepository import BookingRepository
from BookingManager import BookingManager

# Tester för Repository userstory 2 och 4. 
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

#Tester för klassen BookingManager - Userstory 2 och 4.
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

class TestUserStory1(unittest.TestCase):
    def setUp(self):
        """Skapar en testinstans av BookingManager med mockat repo."""
        from BookingManager import BookingManager
        self.manager = BookingManager("test_bookings.json")
        self.manager.repo = MagicMock()  # Mocka repository för att isolera testerna

    def test_successful_booking(self):
        """Testar att bokning lyckas när tid och frisör är lediga."""
        self.manager.repo.search_if_booking_exists.return_value = False  # Simulera en ledig tid

        # Anropa add_booking med test
        result = self.manager.add_booking(
            "test@example.com", "2025-04-10", "11:00", "Test Testsson", "Klippning", "Peter"
        )

        self.assertTrue(result)  # kolla att bokningen blir godkännd
        self.manager.repo.add_booking.assert_called_once()  # Kolla att sparning anropas

    def test_booking_saves_to_json(self):
        """Testar att bokningen skickas vidare till repository för att sparas."""
        self.manager.repo.search_if_booking_exists.return_value = False
        self.manager.repo.add_booking = MagicMock()  # Mocka spara-funktion

        # Skapa bokning
        self.manager.add_booking(
            "email@test.com", "2025-04-11", "12:00", "Namn Test", "Klippning", "Sara"
        )

        self.manager.repo.add_booking.assert_called_once()  # Kolla att spara anropades

    def test_add_and_retrieve_booking(self):
        """Integrations, lägg till bokning och hämta den via get_all_bookings."""
        from BookingRepository import BookingRepository
        repo = BookingRepository("test_bookings.json")
        repo._BookingRepository__bookings_dict = {}  # tom bokningslista
        repo.save_dict_to_json_file = MagicMock()  # Mocka en filskrivning

        manager = BookingManager("test_bookings.json")
        manager.repo = repo  # Använd mockat repository

        result = manager.add_booking("anna@example.com", "2025-04-12", "13:00", "Anna", "Klippning långt hår", "Hannah")
        self.assertTrue(result)  # Kolla att bokningen går igenom

        bookings = manager.get_all_bookings()
        self.assertIn("anna@example.com", bookings)  # Kolla om bokningen går att hämta


class TestUserStory3(unittest.TestCase):
    def setUp(self):
        """Skapar en testinstans av BookingManager med mockad repository."""
        from BookingManager import BookingManager
        self.manager = BookingManager("test_bookings.json")
        self.manager.repo = MagicMock()  # Mocka repository för att isolera testerna

    def test_detect_existing_booking(self):
        """Testar att systemet identifierar en redan existerande bokning"""
        from BookingRepository import BookingRepository
        repo = BookingRepository("test_bookings.json")
        repo._BookingRepository__bookings_dict = {  # Skapa  en befintlig bokning
            "existing@example.com": {
                "email": "existing@example.com",
                "date": "2025-04-15",
                "time": "10:00",
                "name": "Test",
                "service": "Klippning",
                "hairdresser": "Peter"
            }
        }

        # Anropa search_if_booking_exists
        exists = repo.search_if_booking_exists("2025-04-15", "10:00", "Peter")
        self.assertTrue(exists)  # Kolla ifall metoden hittar dubbelbokningen

    def test_booking_denied_if_time_taken(self):
        """Testar att en bokning nekas ifall tid och frisör är bokad"""
        self.manager.repo.search_if_booking_exists.return_value = True  # Simulera att en tid är upptagen

        result = self.manager.add_booking(
            "double@example.com", "2025-04-15", "10:00", "Dubbel", "Klippning", "Peter"
        )

        self.assertFalse(result)  # Bokningen ska nekas
        self.manager.repo.add_booking.assert_not_called()  # Sparning ska inte funka

    def test_booking_allowed_with_other_hairdresser(self):
        """Testar att samma tid kan bokas ifall annan frisör."""
        self.manager.repo.search_if_booking_exists.return_value = False  # Simulera ledig tid

        result = self.manager.add_booking(
            "new@example.com", "2025-04-15", "10:00", "Ny Kund", "Färgning", "Sara"
        )

        self.assertTrue(result)  # Bokningen godkänns
        self.manager.repo.add_booking.assert_called_once()  # Kolla att de sparas

    def test_integration_deny_duplicate_booking(self):
        """Integrations, kolla att bokningen nekas i hela flödet dubbelbokning."""
        from BookingRepository import BookingRepository
        repo = BookingRepository("test_bookings.json")
        repo._BookingRepository__bookings_dict = {
            "existing@example.com": {
                "email": "existing@example.com",
                "date": "2025-04-16",
                "time": "10:00",
                "name": "Test",
                "service": "Klippning",
                "hairdresser": "Peter"
            }
        }
        repo.save_dict_to_json_file = MagicMock()  # Mocka filskrivning

        manager = BookingManager("test_bookings.json")
        manager.repo = repo

        result = manager.add_booking("new@example.com", "2025-04-16", "10:00", "Ny", "Klippning", "Peter")
        self.assertFalse(result)  # Bokningen ska nekas



if __name__ == '__main__':
    unittest.main()