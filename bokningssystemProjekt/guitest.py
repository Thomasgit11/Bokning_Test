import tkinter as tk
from tkinter import ttk, messagebox
from BookingManager import BookingManager

# skapar upp klassen TreeViewBooking
class TreeViewBooking:
    def __init__(self, my_root, booking_manager):  #konstruktormetod.
        my_root.title('Treeview booking')
        my_root.geometry('620x400')
        self.booking_manager = booking_manager  
        
        #anropar metod för att skapa upp textbox_frame och treeview_frame. 
        self.__init_textbox_frame(my_root)   
        self.__init_treeview_frame(my_root)
    
    #frame för labels, knappar och combobox.
    def __init_textbox_frame(self, my_root):
        self.textboxframe = tk.Frame(my_root, highlightbackground="black", highlightthickness=2)
        self.textboxframe.pack(side="top", fill="both", expand=True)

        # Skapa inputfält och labels
        self.email_label = tk.Label(self.textboxframe, text="Epost")
        self.email_label.grid(row=0, column=0)
        self.email_entry = tk.Entry(self.textboxframe)
        self.email_entry.grid(row=0, column=1)

        self.date_label = tk.Label(self.textboxframe, text="Datum (YYYY-MM-DD)")
        self.date_label.grid(row=1, column=0)
        self.date_entry = tk.Entry(self.textboxframe)
        self.date_entry.grid(row=1, column=1)

        self.time_label = tk.Label(self.textboxframe, text="Tid")
        self.time_label.grid(row=2, column=0)
        self.time_combobox = ttk.Combobox(self.textboxframe, values=["10:00", "11:00", "12:00", "13:00", "14:00"])
        self.time_combobox.set("Välj en tid")
        self.time_combobox.grid(row=2, column=1)

        self.name_label = tk.Label(self.textboxframe, text="Namn")
        self.name_label.grid(row=3, column=0)
        self.name_entry = tk.Entry(self.textboxframe)
        self.name_entry.grid(row=3, column=1)

        self.service_label = tk.Label(self.textboxframe, text="Tjänst")
        self.service_label.grid(row=4, column=0)
        self.service_combobox = ttk.Combobox(self.textboxframe, values=["Klippning långt hår", "Klippning kort hår"])
        self.service_combobox.set("Välj tjänst")
        self.service_combobox.grid(row=4, column=1)

        self.hairdresser_label = tk.Label(self.textboxframe, text="Frisör")
        self.hairdresser_label.grid(row=5, column=0)
        self.hairdresser_combobox = ttk.Combobox(self.textboxframe, values=["Peter", "Hannah", "Sara"])
        self.hairdresser_combobox.set("Välj en frisör")
        self.hairdresser_combobox.grid(row=5, column=1)

        # Skapar knappar
        self.add_button = tk.Button(self.textboxframe, text="Lägg till", command=self.add_new_booking)
        self.add_button.grid(row=6, column=0)

        self.show_by_date_button = tk.Button(self.textboxframe, text="Visa bokningar efter datum",
                                             command=self.show_bookings_date)
        self.show_by_date_button.grid(row=6, column=1)

        self.delete_button = tk.Button(self.textboxframe, text="Ta bort", command=self.delete_selected_booking)
        self.delete_button.grid(row=6, column=2)

        self.shutdown_button = tk.Button(self.textboxframe, text="Stäng ner bokningen", command=self.shut_down_program)
        self.shutdown_button.grid(row=6, column=3)

    def __init_treeview_frame(self, my_root):
        #skapa upp en ram för treeview.
        self.treeviewframe = tk.Frame(my_root, highlightbackground="black", highlightthickness=2, pady=13, padx=13)
        self.treeviewframe.pack(side="bottom", fill="both", expand=True)
        #definiera kolumnerna i treeview.
        columns = ['email', 'date', 'time', 'name', 'service', 'hairdresser']
        self.tree = ttk.Treeview(self.treeviewframe, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col.capitalize(), anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER, width=100)
        
        #Hämtar alla bokningar. 
        self.__get_all_bookings()

        # binder en händelsehanterare när man klickar på en rad i treeview,
        # där den valda raden hamnar i entry textfält och combobox.
        self.tree.bind('<<TreeviewSelect>>', self.selected_booking)
        self.tree.grid(row=0, column=0, sticky='nsew')
        
        # Lägger till en scrollbar till treeview i högra hörnet.
        self.scrollbar = ttk.Scrollbar(self.treeviewframe, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
    
    #Funktion för att lägga till en ny bokning. 
    def add_new_booking(self):
        # hämta data från entry textfält och listbox för att lägga till bokning.
        email, date, time, name, service, hairdresser = self.__get_booking_values()
        # lägg till i fil, anropa bookingmanager.
        if self.booking_manager.add_booking(email, date, time, name, service, hairdresser):
            self.tree.insert("", index=0, values=[email, date, time, name, service, hairdresser])
        else:
            #Om bokning redan finns, skriv ut felmeddelande. 
            messagebox.showerror("Bokning finns", "Bokningen finns redan, välj ett annat datum, tid eller frisör.")
    
    #Funktion för att ta bort en vald bokning.
    def delete_selected_booking(self):
        try:
            if messagebox.askyesno("Ta bort?", "Vill du ta bort den här bokningen?"):
                selected_item = self.tree.selection()[0]
                email, *_ = self.tree.item(selected_item)['values']
                self.booking_manager.delete_booking(email)
                self.tree.delete(selected_item)
                # tömmer entry textfält och combobox på den raderade bokningens uppgifter.
                self.email_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)
                self.time_combobox.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.service_combobox.delete(0, tk.END)
                self.hairdresser_combobox.delete(0, tk.END)
        except IndexError:
            messagebox.showerror("Välj bokning", "Välj en bokning i listan")
    
    #Funktion för att visa bokningar på ett valt datum. 
    def show_bookings_date(self):
        selected_date = self.date_entry.get()
        # anropar metod som returnerar matchade bokningar, skickar med datum för matchning.
        found_bookings = self.booking_manager.search_by_date(selected_date)

        self.__clear_treeview()

        if not found_bookings:
            messagebox.showinfo("Inga bokningar ", "Det finns inga bokningar för det valda datumet. ")
            return
        # skriver ut de bokningar som hittats på det valda datumet i treeview.
        for booking in found_bookings.values():
            self.tree.insert('', tk.END, values=(booking['email'], booking['date'], booking['time'],
                                                 booking['name'], booking['service'], booking['hairdresser']))

    def selected_booking(self, event):
        selected_item = self.tree.focus()
        item = self.tree.item(selected_item)['values']
        if item:
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, item[0])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, item[1])
            self.time_combobox.set(item[2])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, item[3])
            self.service_combobox.set(item[4])
            self.hairdresser_combobox.set(item[5])

    def shut_down_program(self):
        if messagebox.askyesno('Avsluta?', 'Vill du avsluta programmet?'):
            root.destroy()

    def __clear_treeview(self):
        for booking in self.tree.get_children():
            self.tree.delete(booking)
    
    # funktion för att hämta alla bokningar från fil
    def __get_all_bookings(self):
        bookings = self.booking_manager.get_all_bookings()
        for booking in bookings.values():
            self.tree.insert('', tk.END, values=(booking['email'], booking['date'], booking['time'],
                                                 booking['name'], booking['service'], booking['hairdresser']))

    def __get_booking_values(self):
        return (self.email_entry.get(), self.date_entry.get(), self.time_combobox.get(), self.name_entry.get(),
                self.service_combobox.get(), self.hairdresser_combobox.get())


if __name__ == "__main__":
    #skapa root fönstret 
    root = tk.Tk()
    #anropa treeview klassen och bookingmanagerklassen, skickar med filen som ska användas. 
    TreeViewBooking(root, BookingManager('bookings.json'))
    root.mainloop()