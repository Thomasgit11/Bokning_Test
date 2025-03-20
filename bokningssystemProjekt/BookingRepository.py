import json  # importerar json.


# Definierar BookingRepository klassen.
class BookingRepository:
    # konstruktormetod, init-metod för att initialisera objekt.
    def __init__(self, file_name):
        self.__file_name = file_name  # fil där bokningar sparas
        self.__bookings_dict = {}  # skapar upp dict för alla bokningar från fil.
        self.load_bookings_from_file()  # anropar funktionen för ladda upp bokningar från fil när objektet skapas.

    # Publika metoder.
    def get_all(self):  # metod som hämtar alla bokningar från fil och returnerar bookings-dict.
        #self.load_bookings_from_file()
        return self.__bookings_dict

    # Metod för att söka efter bokningar baserat på datum från användaren.
    def search_date(self, date):
        found_bookings_dict = {}  # skapar upp en tom dict där bokningar som matchar datum ska läggas till.
        for email, booking in self.__bookings_dict.items():  # går igenom bookings dict efter matchning
            if date in booking["date"]:
                found_bookings_dict[booking["email"]] = booking  # adderar matchade bokningar till dict
        # returnerar dict med matchade bokningar.
        return found_bookings_dict

    def add_booking(self, booking): # Metod som tar emot en bokning och lägger till som en boknings-dict i bookingsdict,
        # där email är bokningens nyckel i bookings-dicten.
        self.__bookings_dict[booking.email] = {
            'email': booking.email,
            'date': booking.date,
            'time': booking.time,
            'name': booking.name,
            'service': booking.service,
            'hairdresser': booking.hairdresser
        }
        self.save_dict_to_json_file()  # sparar ner till json fil för att ny bokning ska sparas.

    # Metod för att kontrollera om bokning med datum, tid och frisör redan finns.

    def search_if_booking_exists(self, date, time, hairdresser):
        # Går igenom bokningar i dicten. Om bokning redan finns med det datum, tid och frisör, returneras True.
        for email, booking in self.__bookings_dict.items():
            if date == booking['date'] and time == booking['time'] and hairdresser == booking['hairdresser']:
                return True

        return False  # om bokning inte finns, returneras False.


    def delete_booking(self, email):  # Metod för att ta bort bokning baserat på emailadress.
        if email in self.__bookings_dict:
            print(f"Deleting booking: {self.__bookings_dict[email]}") #TA BORT SEN. 
            self.__bookings_dict.pop(email)  # Använder pop metoden för att ta bort bokning.
            self.save_dict_to_json_file()  # anropar metoden för att spara ned ändringen..
            return True
        print("No booking found to delete..")
        return False 

    def load_bookings_from_file(self):  # Metod för att läsa in bokningar från json-fil.
        try:
            with open(self.__file_name, 'r') as file_stream:  # provar öppna fil i read läge.
                self.__bookings_dict = json.load(file_stream)  # det som finns i json-fil, läggs till i bookings-dict.

        except FileNotFoundError:
            self.__bookings_dict = {}  # Om filen inte finns, skapa upp en tom dict.

    def save_dict_to_json_file(self):  # Metod för att spara ner bookings-dict till json fil.
        with open(self.__file_name, 'w') as file_stream:  # öppnar filen i write läge.
            json.dump(self.__bookings_dict, file_stream, indent=4)  # använder json dump metod, med indrag.

