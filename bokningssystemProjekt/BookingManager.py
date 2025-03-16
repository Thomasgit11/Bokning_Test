from BookingRepository import BookingRepository
from BookingClass import Booking


class BookingManager:
    def __init__(self, file_name):
        self.repo = BookingRepository(file_name)

    def add_booking(self, email, date, time, name, service, hairdresser):
        if not self.repo.search_if_booking_exists(date, time, hairdresser):
            booking = Booking(email, date, time, name, service, hairdresser)
            self.repo.add_booking(booking)
            return True  # Bokningen lyckades
        return False  # Bokningen fanns redan

    def delete_booking(self, email):
        self.repo.delete_booking(email)

    def get_all_bookings(self):
        return self.repo.get_all()

    def search_by_date(self, date):
        return self.repo.search_date(date)