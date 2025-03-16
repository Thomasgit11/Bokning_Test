class Booking:  # Klass som representerar en bokning
    def __init__(self, email, date, time, name, service, hairdresser):  # initiera instans för booking
        self.email = email  # Lagra email, date, time, name, service, hairdresser
        self.date = date
        self.time = time
        self.name = name
        self.service = service
        self.hairdresser = hairdresser

