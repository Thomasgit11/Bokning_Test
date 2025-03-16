import tkinter as tk # importera tkinter.
from tkinter import ttk
from tkinter import messagebox

# importerar klassen BookingRepository samt klassen Booking.
from BookingRepository import BookingRepository
from BookingClass import Booking


# skapar upp klassen TreeViewBooking
class TreeViewBooking:
    def __init__(self, my_root, booking_repo):  # konstruktormetod, init-metod för att initialisera objekt.
        root.title('Treeview booking')  # Titel för användergränssnitt
        root.geometry('620x400')  # Storlek på fönstret
        self.__BookingRepository = booking_repo

        self.__init_textbox_frame(my_root)  # anropar metoden för att skapa upp textbox_frame
        self.__init_treeview_frame(my_root)  # anropar metoden skapa upp treeview_frame.

    def __init_textbox_frame(self, my_root):  # Frame för labels, knappar, combobox
        self.textboxframe = tk.Frame(my_root, highlightbackground="black", highlightthickness=2)

        self.textboxframe.pack(side="top", fill="both", expand=True)
        # create and add lables and entry textfields
        self.email_label = tk.Label(self.textboxframe, text="Epost")  # skapa label titel epost
        self.email_label.grid(row=0, column=0)  # Placera label
        self.email_entry = tk.Entry(self.textboxframe)  # Input textbox för email
        self.email_entry.grid(row=0, column=1)  # Placera epost entry

        self.date_label = tk.Label(self.textboxframe, text="Datum (YYYY-MM-DD)")  # Label titel "datum yyyy-mm-dd"
        self.date_label.grid(row=1, column=0)  # Placera label
        self.date_entry = tk.Entry(self.textboxframe)  # Input textbox för datum
        self.date_entry.grid(row=1, column=1)  # Placera datum entry

        self.time_label = tk.Label(self.textboxframe, text="Tid")  # label titel  "tid"
        self.time_label.grid(row=2, column=0)  # Placera label
        times = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]  # Lista för värden till combobox
        self.time_combobox = ttk.Combobox(self.textboxframe, values=times)  # Dropdown lista med tider
        self.time_combobox.set("Välj en tid")  # Sätt en förskriven titel i comboboxen för tydlighet
        self.time_combobox.grid(row=2, column=1)  # Placera comboboxen/dropdown

        self.name_label = tk.Label(self.textboxframe, text="Namn")  # label titel "namn"
        self.name_label.grid(row=3, column=0)  # placera label
        self.name_entry = tk.Entry(self.textboxframe)  # input textbox namn
        self.name_entry.grid(row=3, column=1)  # palcera textbox för namn input

        self.service_label = tk.Label(self.textboxframe, text="Tjänst")  # label titel "Tjänst"
        self.service_label.grid(row=4, column=0)  # Placera label
        self.service = ["Klippning långt hår", "Klippning kort hår", "Klippning + färgning"]  # Lista till combobox
        self.service_combobox = ttk.Combobox(self.textboxframe,
                                             values=self.service)  # Combobox/dropdown med olika tjänster
        self.service_combobox.grid(row=4, column=1)  # Placera combobox/dropdown
        self.service_combobox.set("Välj tjänst")  # Sätt förskriven text i combobox för tydlighet

        self.hairdresser_label = tk.Label(self.textboxframe, text="Frisör")  # Skapa label för titel "Frisör"
        self.hairdresser_label.grid(row=5, column=0)  # Placera label
        self.hairdressers = ["Peter", "Hannah", "Sara"]  # Lista med val till combobox
        self.hairdresser_combobox = ttk.Combobox(self.textboxframe,
                                                 values=self.hairdressers)  # Skapar combobox/dropdown
        self.hairdresser_combobox.grid(row=5, column=1)  # Placerar combobox
        self.hairdresser_combobox.set("Välj en frisör")  # Sätter förskriven text i combobox för tydlighet

        # skapar upp en lägg till knapp, kopplar händelsehanterare - anropar metoden som ska köras.
        self.add_button = tk.Button(self.textboxframe, text="Lägg till", command=self.add_new_booking)
        self.add_button.grid(row=6, column=0)  # Placerar knapp

        # skapar upp en knapp för visa bokningar efter datum, kopplar händelsehanterare - anropar metoden som ska köras.
        self.show_by_date_button = tk.Button(self.textboxframe, text="Visa bokningar efter datum",
                                             command=self.show_bookings_date)
        self.show_by_date_button.grid(row=6, column=1)  # Placerar knapp

        # skapar upp en delete knapp, kopplar händelsehanterare - anropar metoden som ska köras.
        self.delete_button = tk.Button(self.textboxframe, text="Ta bort", command=self.delete_selected_booking)
        self.delete_button.grid(row=6, column=2)  # Placerar knapp

        # skapar upp en avsluta program knapp, kopplar händelsehanterare - anropar metoden som ska köras.
        self.shutdown_button = tk.Button(self.textboxframe, text="Stäng ner bokningen", command=self.shut_down_program)
        self.shutdown_button.grid(row=6, column=3)  # Placerar knapp

    def __init_treeview_frame(self, my_root):
        # Skapa en ram för treeview
        self.treeviewframe = tk.Frame(my_root, highlightbackground="black", highlightthickness=2, pady=13, padx=13)
        self.treeviewframe.pack(side="bottom", fill="both", expand=True)
        # Definera de lika kolumnerna i treeview
        columns = ['email', 'date', 'time', 'name', 'service', 'hairdresser']
        # Skapa treeview
        self.tree = ttk.Treeview(self.treeviewframe, columns=columns, show='headings')

        # Skapa rubriker i treeview samt centrera dem i varje kolumn
        # Rubriker, #Epost, Datum, Tid, Namn, Tjänst, Frisör
        self.tree.heading('email', text='Epost', anchor=tk.CENTER)
        self.tree.heading('date', text='Datum', anchor=tk.CENTER)
        self.tree.heading('time', text='Tid', anchor=tk.CENTER)
        self.tree.heading('name', text='Namn', anchor=tk.CENTER)
        self.tree.heading('service', text='Tjänst', anchor=tk.CENTER)
        self.tree.heading('hairdresser', text='Frisör', anchor=tk.CENTER)

        # Formaterar kolumnerna från oven,
        self.tree.column('email', width=100, stretch=tk.NO)
        self.tree.column('date', anchor=tk.CENTER, width=100)
        self.tree.column('time', anchor=tk.CENTER, width=100)
        self.tree.column('name', anchor=tk.CENTER, width=100)
        self.tree.column('service', anchor=tk.CENTER, width=100)
        self.tree.column('hairdresser', anchor=tk.CENTER, width=100)

        # Hämtar alla bokningar och fyller treeview.
        self.__get_all_bookings()

        # binder en händelsehanterare när man klickar på en rad i treeview,
        # där den valda raden hamnar i entry textfält och combobox.
        self.tree.bind('<<TreeviewSelect>>', self.selected_booking)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Lägger till en scrollbar till treeview i högra hörnet.
        self.scrollbar = ttk.Scrollbar(self.treeviewframe, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

    def add_new_booking(self):  # Def för att lägga till ny bokning
        # hämta data från entry textfält och listbox för att lägga till bokning.
        email, date, time, name, service, hairdresser = self.__get_booking_values()
        # om bokning med det datum, tid och frisör inte finns, lägg till.
        if not self.__BookingRepository.search_if_booking_exists(date, time, hairdresser):
            # lägg till i fil, anropa repositoryklassen.
            self.__BookingRepository.add_booking(Booking(email, date, time, name, service, hairdresser))
            #  lägg till i treeview.
            self.tree.insert("", index=0, values=[email, date, time, name, service, hairdresser])

        else:  # om bokning redan finns, visa felmeddelande.
            messagebox.showerror("Bokning finns", "Bokningen finns redan, prova med ett annat datum, tid eller frisör.")

    def delete_selected_booking(self):  # Def för att ta bort vald bokning
        try:  # Meddelande om man verkligen vill ta bort den valda bokningen
            if messagebox.askyesno("Ta bort?", "Vill du ta bort den här bokningen?"):
                selected_item = self.tree.selection()[0]
                email, date, time, name, service, hairdresser = self.__get_booking_values()
                self.__BookingRepository.delete_booking(email)  # Ta bort från jsonfil.
                self.tree.delete(selected_item)  # ta bort från treeview.
                # tömmer entry textfält och combobox på den raderade bokningens uppgifter.
                self.email_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)
                self.time_combobox.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.service_combobox.delete(0, tk.END)
                self.hairdresser_combobox.delete(0, tk.END)

        except IndexError:  # Error meddelande
            messagebox.showerror("Välj bokning", "Välj den bokning du vill ta bort i listan")

    def show_bookings_date(self):  # Sökfunktion för att visa bokningar visst datum
        # ta det valda datumet.
        selected_date = self.__get_date_value()
        # anropar metod i repository som returnerar matchade bokningar, skickar med datum för matchning.
        found_bookings = self.__BookingRepository.search_date(selected_date)

        self.__clear_treeview()  # anropar metod som tömmer treeview.

        # skriver ut de bokningar som hittats på det valda datumet i treeview.
        for index, booking in found_bookings.items():
            self.tree.insert('', tk.END, text=f'Booking {index}', values=(booking['email'], booking['date'],
                                                                          booking['time'], booking['name'],
                                                                          booking['service'],
                                                                          booking['hairdresser']))

    def selected_booking(self, event):  # Def för att hantera vald bokning
        selected_item = self.tree.focus()  # selected_item är den rad (bokning) användaren tryckt på i treeview.
        item = self.tree.item(selected_item)
        row_data_item = item['values']
        # anropar metoden fill_booking_values och skickar med data för raden(bokning).
        self.__fill_booking_values(row_data_item)

    def shut_down_program(self):  # Def för att stänga av programmet, samt bekräftelse meddelande
        if messagebox.askyesno('Avsluta?', 'Vill du avsluta programmet?'):
            root.destroy()

    def __fill_booking_values(self, row_data_bookings):  # De för att fylla i textfält med relevent bokningsinfo
        # när användaren trycker på en bokning i treeview.
        if len(row_data_bookings) != 0:
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, row_data_bookings[0])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, row_data_bookings[1])
            self.time_combobox.delete(0, tk.END)
            self.time_combobox.insert(0, row_data_bookings[2])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, row_data_bookings[3])
            self.service_combobox.delete(0, tk.END)
            self.service_combobox.insert(0, row_data_bookings[4])
            self.hairdresser_combobox.delete(0, tk.END)
            self.hairdresser_combobox.insert(0, row_data_bookings[5])

    def __get_booking_values(self):  # def för att returnera input värden
        # Returnerar entries från alla textfält
        return (self.email_entry.get(), self.date_entry.get(), self.time_combobox.get(), self.name_entry.get(),
                self.service_combobox.get(), self.hairdresser_combobox.get())

    def __get_date_value(self):  # Def för att returnera specifikt datum entry
        return self.date_entry.get()

    def __clear_treeview(self):  # Def för att tömma bort alla bokingar ur treeview
        bookings = self.tree.get_children()  # hämtar alla bokningar som finns i treeview.
        for booking in bookings:  # loopar igenom varje bokning och tar bort den ur treeview.
            self.tree.delete(booking)

    def __get_all_bookings(self):  # def för att hämta alla bokningar från fil
        # hämtar alla bokningar från json fil.
        bookings = self.__BookingRepository.get_all()

        # loop för att lägga till alla bokningar i treeview.
        for index, booking in bookings.items():
            self.tree.insert('', tk.END, text=f'Booking {index}', values=(booking['email'], booking['date'],
                                                                          booking['time'], booking['name'],
                                                                          booking['service'], booking['hairdresser']))


if __name__ == "__main__":
    # Skapa root fönstret
    root = tk.Tk()
    # anropa treeview klassen och repository klassen och skickar med den jsonfil som ska användas.
    TreeViewBooking(root, BookingRepository('bookings.json'))
    # Starta event loopen
    root.mainloop()



    