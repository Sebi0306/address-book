from tkinter import *
from tkinter import font as tkFont, messagebox
import sqlite3

# Main window
root = Tk()
root.title("  Address book")
root.geometry("680x520")
root.iconbitmap("address_book_icon.ico")

# Global variables
load_record_id = 0

# Padding variables
frame_padx = 15
frame_pady = 20

label_pady = 8
entry_pady = 8

# Dimension variables
entry_width = 22

# Fonts
frame_font = tkFont.Font(family='Calibri', size=12)
button_font = tkFont.Font(family='Calibri', size=11)
label_font = tkFont.Font(family='Arial', size=10)

# Frames
input_data_frame = LabelFrame(root, text="Input Data", font=frame_font, padx=frame_padx, pady=frame_pady)
input_data_frame.grid(row=0, column=0, padx=(60, 20), pady=20)

options_frame = LabelFrame(root, text="Options", font=frame_font, padx=frame_padx, pady=20)
options_frame.grid(row=0, column=1, sticky=N+S, padx=20, pady=20)

display_data_frame = Frame(root)

# Connect to address_book DB
connection_main_var = sqlite3.connect('address_book.db')
# Create cursor
cursor_main_var = connection_main_var.cursor()

# Create table
cursor_main_var.execute('''CREATE TABLE IF NOT EXISTS addresses(
    first_name text,
    last_name text,
    address text,
    city text,
    county text,
    zip_code integer)
''')

# Submit record to database function
def submit_record():
    # Global variables
    global display_data_frame, entries_list, labels_list
    # Connect to address_book DB
    connection_var = sqlite3.connect('address_book.db')
    # Create cursor
    cursor_var = connection_var.cursor()
    # Check if any entry is empty
    if first_name_entry.get() == "" or last_name_entry.get() == "" or address_entry.get() == "" or city_entry.get() == "" or county_entry.get() == "" or zip_code_entry.get() == "":
        messagebox.showerror("Missing text error", "Please fill in all entries!")
        for entry in entries_list:
            if entry.get() == "":
                labels_list[entries_list.index(entry)].configure(fg="red")
    # If all entries are completed by the user, the record will be inserted
    else:
        # Insert into table
        cursor_var.execute("INSERT INTO addresses VALUES (:first_name, :last_name, :address, :city, :county, :zip_code)",
                        {
                            'first_name': first_name_entry.get(),
                            'last_name': last_name_entry.get(),
                            'address': address_entry.get(),
                            'city': city_entry.get(),
                            'county': county_entry.get(),
                            'zip_code': zip_code_entry.get()
                        }
        )
        # Remake the labels text black
        for entry in entries_list:
            if entry.get() != "":
                labels_list[entries_list.index(entry)].configure(fg="black")
        # Delete display_data_frame widgets
        total_entries = display_data_frame.grid_slaves()
        for entr in total_entries:
            entr.destroy()
        # Update table
        column_id = ["ID", "First Name", "Last Name", "Address", "City", "County", "Zip Code"]
        # Draw table head
        for c_id in column_id:
            table_label = Label(display_data_frame, text=c_id)
            table_label.grid(row=0, column=column_id.index(c_id), sticky=W, pady=5)
        # Display data
        cursor_var.execute("SELECT oid, * FROM addresses")
        total_records = cursor_var.fetchall()
        for single_record in total_records:
            print(single_record)
            for element in single_record:
                table_entry = Entry(display_data_frame, bg="gray99")
                if single_record.index(element) == 0:
                    table_entry.configure(width=7)
                elif single_record.index(element) == 1:
                    table_entry.configure(width=12)
                elif single_record.index(element) == 5 or single_record.index(element) == 6:
                    table_entry.configure(width=10)
                else:
                    table_entry.configure(width=17)
                table_entry.insert(0, element)
                table_entry.grid(row=total_records.index(single_record) + 1, column=single_record.index(element), sticky=W)
        # Make the data frame visible
        display_data_frame.grid(row=1, column=0, columnspan=2, padx=(40, 0), pady=20)
        # Clear text boxes
        first_name_entry.delete(0, END)
        last_name_entry.delete(0, END)
        address_entry.delete(0, END)
        city_entry.delete(0, END)
        county_entry.delete(0, END)
        zip_code_entry.delete(0, END)
        # Commit
        connection_var.commit()
    # Close connection from DB
    connection_var.close()


# Show records function
def show_records():
    # Connect to address_book DB
    connection_var = sqlite3.connect('address_book.db')
    # Create cursor
    cursor_var = connection_var.cursor()
    # Place display_data_frame
    display_data_frame.grid(row=1, column=0, columnspan=2, padx=(40, 0), pady=20)
    # Update records table
    cursor_var.execute("SELECT oid, * FROM addresses")
    total_records = cursor_var.fetchall()
    print(total_records)
    total_entries = display_data_frame.grid_slaves()
    for entr in total_entries:
        entr.destroy()
    # Check if total_records list is empty
    if total_records == []:
        messagebox.showwarning("Database Empty", "There are no records to display!")
    else:
        column_id = ["ID", "First Name", "Last Name", "Address", "City", "County", "Zip Code"]
        # Draw table head
        for c_id in column_id:
            table_label = Label(display_data_frame, text=c_id)
            table_label.grid(row=0, column=column_id.index(c_id), sticky=W, pady=5)
        # Display data
        for single_record in total_records:
            print(single_record)
            for element in single_record:
                table_entry = Entry(display_data_frame, bg="gray99")
                if single_record.index(element) == 0:
                    table_entry.configure(width=7)
                elif single_record.index(element) == 1:
                    table_entry.configure(width=12)
                elif single_record.index(element) == 5 or single_record.index(element) == 6:
                    table_entry.configure(width=10)
                else:
                    table_entry.configure(width=17)
                table_entry.insert(0, element)
                table_entry.grid(row=total_records.index(single_record)+1, column=single_record.index(element), sticky=W)
    # Commit
    connection_var.commit()
    # Close connection from DB
    connection_var.close()


# Delete Element function
def delete_record():
    global display_data_frame
    global load_record_id
    # Connect to address_book DB
    connection_var = sqlite3.connect('address_book.db')
    # Create cursor
    cursor_var = connection_var.cursor()
    # Delete Record
    cursor_var.execute("DELETE from addresses WHERE oid=" + str(load_record_id))
    print(load_record_id)
    # Delete display_data_frame widgets
    total_entries = display_data_frame.grid_slaves()
    for entr in total_entries:
        entr.destroy()
    # Load data into total_records list
    cursor_var.execute("SELECT oid, * FROM addresses")
    total_records = cursor_var.fetchall()
    # Check if the list is empty
    if total_records != []:
        # Update table
        column_id = ["ID", "First Name", "Last Name", "Address", "City", "County", "Zip Code"]
        # Draw table head
        for c_id in column_id:
            table_label = Label(display_data_frame, text=c_id)
            table_label.grid(row=0, column=column_id.index(c_id), sticky=W, pady=5)
        # Display data
        for single_record in total_records:
            print(single_record)
            for element in single_record:
                table_entry = Entry(display_data_frame, bg="gray99")
                if single_record.index(element) == 0:
                    table_entry.configure(width=7)
                elif single_record.index(element) == 1:
                    table_entry.configure(width=12)
                elif single_record.index(element) == 5 or single_record.index(element) == 6:
                    table_entry.configure(width=10)
                else:
                    table_entry.configure(width=17)
                table_entry.insert(0, element)
                table_entry.grid(row=total_records.index(single_record) + 1, column=single_record.index(element),
                                 sticky=W)
        display_data_frame.grid(row=1, column=0, columnspan=2, padx=(40, 0), pady=20)
    # Commit
    connection_var.commit()
    # Close connection from DB
    connection_var.close()
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    address_entry.delete(0, END)
    city_entry.delete(0, END)
    county_entry.delete(0, END)
    zip_code_entry.delete(0, END)


def load_record():
    update_record_window = Tk()
    update_record_window.title("  Load Record")
    update_record_window.geometry("250x140")
    update_record_window.iconbitmap("load_record_icon.ico")
    # Create label
    select_record_label = Label(update_record_window, text="Please enter record ID:")
    select_record_label.grid(row=0, column=0, padx=(40, 0), pady=(30, 0))
    # Create entry
    select_element_entry = Entry(update_record_window, width=5)
    select_element_entry.grid(row=0, column=1, padx=5, pady=(30, 0))

    def confirmation():
        global load_record_id
        load_record_id = select_element_entry.get()
        print(load_record_id)
        update_record_window.destroy()
        # Connect to address_book DB
        connection_var = sqlite3.connect('address_book.db')
        # Create cursor
        cursor_var = connection_var.cursor()
        # Select record from database
        cursor_var.execute("SELECT * FROM addresses WHERE oid="+load_record_id)
        # Save record elements into a list
        load_record_element_list = cursor_var.fetchall()
        first_name_entry.insert(0, load_record_element_list[0][0])
        last_name_entry.insert(0, load_record_element_list[0][1])
        address_entry.insert(0, load_record_element_list[0][2])
        city_entry.insert(0, load_record_element_list[0][3])
        county_entry.insert(0, load_record_element_list[0][4])
        zip_code_entry.insert(0, load_record_element_list[0][5])
        # Delete display_data_frame widgets
        total_entries = display_data_frame.grid_slaves()
        for entr in total_entries:
            entr.destroy()
        # Redraw table and highlight the selected record
        column_id = ["ID", "First Name", "Last Name", "Address", "City", "County", "Zip Code"]
        # Draw table head
        for c_id in column_id:
            table_label = Label(display_data_frame, text=c_id)
            table_label.grid(row=0, column=column_id.index(c_id), sticky=W, pady=5)
        # Display data
        cursor_var.execute("SELECT oid, * FROM addresses")
        total_records = cursor_var.fetchall()
        for single_record in total_records:
            for element in single_record:
                if int(single_record[0]) == int(load_record_id):
                    table_entry = Entry(display_data_frame, bg="gray85")
                else:
                    table_entry = Entry(display_data_frame, bg="gray99")
                if single_record.index(element) == 0:
                    table_entry.configure(width=7)
                elif single_record.index(element) == 1:
                    table_entry.configure(width=12)
                elif single_record.index(element) == 5 or single_record.index(element) == 6:
                    table_entry.configure(width=10)
                else:
                    table_entry.configure(width=17)
                table_entry.insert(0, element)
                table_entry.grid(row=total_records.index(single_record) + 1, column=single_record.index(element),
                                 sticky=W)
        display_data_frame.grid(row=1, column=0, columnspan=2, padx=(40, 0), pady=20)
        # Commit
        connection_var.commit()
        # Close connection from DB
        connection_var.close()
        
    # Confirmation button
    confirmation_button = Button(update_record_window, text="OK", width=8, command=confirmation)
    confirmation_button.grid(row=1, column=0, padx=(40, 0), pady=(18, 0), columnspan=2)


def update_record():
    global load_record_id
    global display_data_frame
    # Connect to address_book DB
    connection_var = sqlite3.connect('address_book.db')
    # Create cursor
    cursor_var = connection_var.cursor()
    cursor_var.execute("""UPDATE addresses SET
        first_name = :first_n,
        last_name = :last_n,
        address = :addr,
        city = :city,
        county = :cnty,
        zip_code = :zip
        WHERE oid = :oid""",
            {
                'first_n': first_name_entry.get(),
                'last_n': last_name_entry.get(),
                'addr': address_entry.get(),
                'city': city_entry.get(),
                'cnty': county_entry.get(),
                'zip': zip_code_entry.get(),
                'oid': load_record_id
            }
        )
    # Delete display_data_frame widgets
    total_entries = display_data_frame.grid_slaves()
    for entr in total_entries:
        entr.destroy()
    # Load data into total_records list
    cursor_var.execute("SELECT oid, * FROM addresses")
    total_records = cursor_var.fetchall()
    #  --- Update table ---
    # Draw table head
    column_id = ["ID", "First Name", "Last Name", "Address", "City", "County", "Zip Code"]
    for c_id in column_id:
        table_label = Label(display_data_frame, text=c_id)
        table_label.grid(row=0, column=column_id.index(c_id), sticky=W, pady=5)
    # Display data
    for single_record in total_records:
        print(single_record)
        for element in single_record:
            table_entry = Entry(display_data_frame, bg="gray99")
            if single_record.index(element) == 0:
                table_entry.configure(width=7)
            elif single_record.index(element) == 1:
                table_entry.configure(width=12)
            elif single_record.index(element) == 5 or single_record.index(element) == 6:
                table_entry.configure(width=10)
            else:
                table_entry.configure(width=17)
            table_entry.insert(0, element)
            table_entry.grid(row=total_records.index(single_record) + 1, column=single_record.index(element),
                             sticky=W)
    # Commit
    connection_var.commit()
    # Close connection from DB
    connection_var.close()
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    address_entry.delete(0, END)
    city_entry.delete(0, END)
    county_entry.delete(0, END)
    zip_code_entry.delete(0, END)


# Labels
first_name_label = Label(input_data_frame, text="First Name:", font=label_font)
first_name_label.grid(row=0, column=0, padx=(0, 15), pady=(5, label_pady))

last_name_label = Label(input_data_frame, text="Last Name:", font=label_font)
last_name_label.grid(row=1, column=0, padx=(0, 15), pady=label_pady)

address_label = Label(input_data_frame, text="Address:", font=label_font)
address_label.grid(row=2, column=0, padx=(0, 15), pady=label_pady)

city_label = Label(input_data_frame, text="City:", font=label_font)
city_label.grid(row=3, column=0, padx=(0, 15), pady=label_pady)

county_label = Label(input_data_frame, text="County:", font=label_font)
county_label.grid(row=4, column=0, padx=(0, 15), pady=label_pady)

zip_code_label = Label(input_data_frame, text="Zip Code:", font=label_font)
zip_code_label.grid(row=5, column=0, padx=(0, 15), pady=label_pady)

show_records_label = Label(root, text="", anchor=W)
show_records_label.grid(row=6, column=1, pady=5, sticky=W)

# Entries
first_name_entry = Entry(input_data_frame, width=entry_width)
first_name_entry.grid(row=0, column=1, padx=0, pady=(5, entry_pady))

last_name_entry = Entry(input_data_frame, width=entry_width)
last_name_entry.grid(row=1, column=1, padx=0, pady=entry_pady)

address_entry = Entry(input_data_frame, width=entry_width)
address_entry.grid(row=2, column=1, padx=0, pady=entry_pady)

city_entry = Entry(input_data_frame, width=entry_width)
city_entry.grid(row=3, column=1, padx=0, pady=entry_pady)

county_entry = Entry(input_data_frame, width=entry_width)
county_entry.grid(row=4, column=1, padx=0, pady=entry_pady)

zip_code_entry = Entry(input_data_frame, width=entry_width)
zip_code_entry.grid(row=5, column=1, padx=0, pady=entry_pady)

# Buttons
submit_record_button = Button(options_frame, text="Add record to database", font=button_font, width=20, command=submit_record)
submit_record_button.grid(row=0, column=0, padx=15, pady=(5, 0))

show_records_button = Button(options_frame, text="Show records", font=button_font, width=20, command=show_records)
show_records_button.grid(row=1, column=0, padx=15, pady=(10, 0))

code_test_button = Button(options_frame, text="Load Record", font=button_font, width=20, command=load_record)
code_test_button.grid(row=2, column=0, pady=(10, 0))

update_record_button = Button(options_frame, text="Update record", font=button_font, width=20, command=update_record)
update_record_button.grid(row=3, column=0, pady=(10, 0))

delete_record_button = Button(options_frame, text="Delete record", font=button_font, width=20, command=delete_record)
delete_record_button.grid(row=4, column=0, pady=(10, 0))

# Global lists
entries_list = [first_name_entry, last_name_entry, address_entry, city_entry, county_entry, zip_code_entry]
labels_list = [first_name_label, last_name_label, address_label, city_label, county_label, zip_code_label]

# Commit
connection_main_var.commit()
# Close connection from DB
connection_main_var.close()

root.mainloop()
